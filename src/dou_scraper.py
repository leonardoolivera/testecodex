"""
Scraper para Diário Oficial da União (DOU)
Busca por publicações do Instituto Federal de Mato Grosso do Sul
"""

import requests
from datetime import datetime, date
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


class DOUScraper:
    """
    Classe para fazer scraping do Diário Oficial da União
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = []

    def search_dou(self, keyword: str, pages: int = 5,
                   start_date: Optional[date] = None,
                   end_date: Optional[date] = None) -> List[Dict]:
        """
        Busca no DOU por um termo específico, com filtro opcional de data.

        Args:
            keyword: Palavra-chave para buscar
            pages: Número de páginas para buscar
            start_date: Data inicial do filtro
            end_date: Data final do filtro

        Returns:
            Lista de dicionários com os resultados
        """
        logger.info(f"Buscando: '{keyword}'" + (
            f" | {start_date} → {end_date}" if start_date else ""
        ))
        all_results = []

        for page in range(pages):
            try:
                params = {
                    'q': keyword,
                    'p': page,
                    'rows': 20,
                    'sort': f"{SORT_BY} {ORDER}",
                    'filtros': '',
                }

                if start_date:
                    params['startDate'] = start_date.strftime('%d-%m-%Y')
                if end_date:
                    params['endDate'] = end_date.strftime('%d-%m-%Y')

                response = self.session.get(DOU_API_URL, params=params, timeout=TIMEOUT)
                response.raise_for_status()

                data = response.json()

                if 'docs' in data:
                    for doc in data['docs']:
                        result = self._parse_document(doc)
                        if result:
                            all_results.append(result)

                if len(data.get('docs', [])) == 0:
                    break

            except requests.RequestException as e:
                logger.error(f"Erro na página {page + 1}: {e}")
                continue
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao decodificar JSON: {e}")
                continue

        return all_results

    def _parse_document(self, doc: Dict) -> Optional[Dict]:
        """
        Extrai informações relevantes de um documento
        """
        try:
            titulo = doc.get('titulo', '').strip()
            url = doc.get('url', '')

            if not titulo or not url:
                return None

            return {
                'data_publicacao': doc.get('data_publicacao', ''),
                'titulo': titulo,
                'secao': doc.get('secao', '').strip(),
                'pagina': str(doc.get('pagina', '')).strip(),
                'url': url,
                'orgao': doc.get('orgao', '').strip(),
                'resumo': (doc.get('ementa', '') or '')[:200].strip(),
                'data_coleta': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Erro ao fazer parsing do documento: {e}")
            return None

    def scrape_all_keywords(self, start_date: Optional[date] = None,
                            end_date: Optional[date] = None) -> List[Dict]:
        """
        Realiza busca para todas as palavras-chave configuradas.
        """
        all_results = []

        for keyword in SEARCH_KEYWORDS:
            results = self.search_dou(keyword, pages=5,
                                      start_date=start_date, end_date=end_date)
            all_results.extend(results)
            logger.info(f"{len(results)} resultado(s) para '{keyword}'")

        # Remove duplicatas por URL
        unique_results = []
        seen_urls = set()
        for result in all_results:
            if result['url'] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result['url'])

        logger.info(f"Total único: {len(unique_results)}")
        self.results = unique_results
        return unique_results

    def filter_by_content_keywords(self) -> List[Dict]:
        """
        Filtra resultados que realmente mencionam IFMS no título, resumo ou órgão.
        """
        keywords_lower = [k.lower() for k in SEARCH_KEYWORDS]
        filtered = [
            r for r in self.results
            if any(
                kw in r['titulo'].lower() or
                kw in r['resumo'].lower() or
                kw in r['orgao'].lower()
                for kw in keywords_lower
            )
        ]

        logger.info(f"Após filtro de conteúdo: {len(filtered)}")
        self.results = filtered
        return filtered

    def filter_by_date_range(self, start_date: date, end_date: date) -> List[Dict]:
        """
        Filtra resultados dentro de um intervalo de datas (fallback cliente).
        Suporta formatos DD/MM/YYYY e YYYY-MM-DD.
        """
        filtered = []
        for r in self.results:
            pub = r.get('data_publicacao', '')
            parsed = _parse_date(pub)
            if parsed and start_date <= parsed <= end_date:
                filtered.append(r)

        logger.info(f"Após filtro de data ({start_date} → {end_date}): {len(filtered)}")
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
    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y'):
        try:
            return datetime.strptime(value[:10], fmt).date()
        except (ValueError, TypeError):
            continue
    return None
