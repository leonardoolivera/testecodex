"""
Scraper para Diário Oficial da União (DOU)
Busca publicações do IFMS via leiturajornal (endpoint oficial do in.gov.br)
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import json
import logging
from typing import List, Dict, Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.config import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Seções do DOU
SECOES = ['do1', 'do2', 'do3']
BASE_ARTICLE_URL = 'https://www.in.gov.br/en/web/dou/-/'
LEITURAJORNAL_URL = 'https://www.in.gov.br/leiturajornal'


class DOUScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9',
        })
        self.results = []

    def fetch_day(self, ref_date: date) -> List[Dict]:
        """
        Busca todas as publicações de um dia específico em todas as seções.
        """
        all_items = []
        data_str = ref_date.strftime('%d-%m-%Y')

        for secao in SECOES:
            try:
                logger.info(f"Buscando {data_str} | seção {secao}")
                items = self._fetch_section(data_str, secao)
                all_items.extend(items)
                logger.info(f"  {len(items)} item(ns) em {secao}")
            except Exception as e:
                logger.warning(f"Erro em {secao} / {data_str}: {e}")

        return all_items

    def _fetch_section(self, data_str: str, secao: str) -> List[Dict]:
        """
        Busca o leiturajornal para uma data e seção específica.
        Extrai o JSON embutido no <script id='params'>.
        """
        url = f"{LEITURAJORNAL_URL}?data={data_str}&secao={secao}"
        response = self.session.get(url, timeout=TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', {'id': 'params'})

        if not script_tag or not script_tag.string:
            logger.debug(f"Sem dados para {secao} em {data_str}")
            return []

        data = json.loads(script_tag.string)
        json_array = data.get('jsonArray', [])

        items = []
        for item in json_array:
            parsed = self._parse_item(item, data_str, secao)
            if parsed:
                items.append(parsed)

        return items

    def _parse_item(self, item: dict, data_str: str, secao: str) -> Optional[Dict]:
        """
        Normaliza os campos de um item do jsonArray.
        """
        try:
            url_title = item.get('urlTitle', '')
            if not url_title:
                return None

            titulo = (
                item.get('title') or
                item.get('titulo') or
                item.get('subtitulo') or
                url_title
            ).strip()

            orgao = (
                item.get('orgao') or
                item.get('organizacao') or
                item.get('hierarchyStr') or
                ''
            ).strip()

            resumo = (
                item.get('ementa') or
                item.get('resumo') or
                item.get('content') or
                ''
            )
            if resumo:
                resumo = resumo[:300].strip()

            return {
                'data_publicacao': data_str,
                'titulo': titulo,
                'secao': secao.upper(),
                'pagina': str(item.get('pagina') or item.get('numberPage') or ''),
                'url': BASE_ARTICLE_URL + url_title,
                'orgao': orgao,
                'resumo': resumo,
                'data_coleta': datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Erro ao parsear item: {e}")
            return None

    def scrape_all_keywords(self, start_date: Optional[date] = None,
                            end_date: Optional[date] = None) -> List[Dict]:
        """
        Busca publicações no intervalo de datas (padrão: hoje).
        """
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = date.today()

        all_results = []
        current = start_date

        while current <= end_date:
            # DOU só publica em dias úteis (seg-sex)
            if current.weekday() < 5:
                items = self.fetch_day(current)
                all_results.extend(items)
            current += timedelta(days=1)

        # Remove duplicatas por URL
        seen = set()
        unique = []
        for r in all_results:
            if r['url'] not in seen:
                unique.append(r)
                seen.add(r['url'])

        logger.info(f"Total único no período: {len(unique)}")
        self.results = unique
        return unique

    def filter_by_content_keywords(self) -> List[Dict]:
        """
        Filtra resultados que mencionam IFMS no título, resumo ou órgão.
        """
        keywords_lower = [k.lower() for k in SEARCH_KEYWORDS]
        filtered = [
            r for r in self.results
            if any(
                kw in r.get('titulo', '').lower() or
                kw in r.get('resumo', '').lower() or
                kw in r.get('orgao', '').lower()
                for kw in keywords_lower
            )
        ]

        logger.info(f"Após filtro de conteúdo: {len(filtered)}")
        self.results = filtered
        return filtered

    def filter_by_date_range(self, start_date: date, end_date: date) -> List[Dict]:
        """
        Filtro de data adicional (já garantido pelo scrape_all_keywords, mas mantido por segurança).
        """
        filtered = []
        for r in self.results:
            parsed = _parse_date(r.get('data_publicacao', ''))
            if parsed is None or start_date <= parsed <= end_date:
                filtered.append(r)

        logger.info(f"Após filtro de data: {len(filtered)}")
        self.results = filtered
        return filtered

    def export_to_json(self, filename: str = 'results.json'):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            logger.info(f"Exportado para {filename}")
        except Exception as e:
            logger.error(f"Erro ao exportar JSON: {e}")


def _parse_date(value: str) -> Optional[date]:
    """Tenta converter string de data para objeto date."""
    if not value:
        return None
    value = str(value).strip()[:10]
    for fmt in ('%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d'):
        try:
            return datetime.strptime(value, fmt).date()
        except (ValueError, TypeError):
            continue
    return None
