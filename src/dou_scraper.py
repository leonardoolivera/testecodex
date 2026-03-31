"""
Scraper para Diário Oficial da União (DOU)
Busca por publicações do Instituto Federal de Mato Grosso do Sul
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import logging
from typing import List, Dict
import sys
import os

# Adiciona o diretório pai ao path para importar config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.config import *

# Configurar logging
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
    
    def search_dou(self, keyword: str, pages: int = 5) -> List[Dict]:
        """
        Busca no DOU por um termo específico
        
        Args:
            keyword: Palavra-chave para buscar
            pages: Número de páginas para buscar
            
        Returns:
            Lista de dicionários com os resultados
        """
        logger.info(f"Iniciando busca por: {keyword}")
        all_results = []
        
        for page in range(pages):
            try:
                # Parâmetros da busca
                params = {
                    'q': keyword,
                    'p': page,
                    'rows': 10,
                    'sort': f"{SORT_BY} {ORDER}",
                    'filtros': '',
                }
                
                logger.info(f"Buscando página {page + 1} para '{keyword}'")
                response = self.session.get(DOU_API_URL, params=params, timeout=TIMEOUT)
                response.raise_for_status()
                
                data = response.json()
                
                # Processa os resultados
                if 'docs' in data:
                    for doc in data['docs']:
                        result = self._parse_document(doc)
                        if result:
                            all_results.append(result)
                            logger.debug(f"Documento encontrado: {result['titulo']}")
                
                # Se não há mais resultados, para a busca
                if len(data.get('docs', [])) == 0:
                    logger.info(f"Nenhum resultado na página {page + 1}")
                    break
                    
            except requests.RequestException as e:
                logger.error(f"Erro ao buscar página {page + 1}: {e}")
                continue
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao decodificar JSON: {e}")
                continue
        
        return all_results
    
    def _parse_document(self, doc: Dict) -> Dict:
        """
        Extrai informações relevantes de um documento
        
        Args:
            doc: Documento JSON do DOU
            
        Returns:
            Dicionário com as informações extraídas
        """
        try:
            # Extrai e limpa os dados
            titulo = doc.get('titulo', '').strip()
            secao = doc.get('secao', '').strip()
            pagina = str(doc.get('pagina', '')).strip()
            data_pub = doc.get('data_publicacao', '')
            url = doc.get('url', '')
            orgao = doc.get('orgao', '').strip()
            ementa = doc.get('ementa', '').strip()
            
            # Valida se tem conteúdo mínimo
            if not titulo or not url:
                return None
            
            return {
                'data_publicacao': data_pub,
                'titulo': titulo,
                'secao': secao,
                'pagina': pagina,
                'url': url,
                'orgao': orgao,
                'resumo': ementa[:200] if ementa else '',  # Resumo dos primeiros 200 caracteres
                'data_coleta': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao fazer parsing do documento: {e}")
            return None
    
    def scrape_all_keywords(self) -> List[Dict]:
        """
        Realiza busca para todas as palavras-chave configuradas
        
        Returns:
            Lista consolidada de resultados
        """
        all_results = []
        
        for keyword in SEARCH_KEYWORDS:
            results = self.search_dou(keyword, pages=5)
            all_results.extend(results)
            logger.info(f"Encontrados {len(results)} resultados para '{keyword}'")
        
        # Remove duplicatas mantendo a ordem
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            if result['url'] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result['url'])
        
        logger.info(f"Total de resultados únicos: {len(unique_results)}")
        self.results = unique_results
        return unique_results
    
    def filter_by_content_keywords(self) -> List[Dict]:
        """
        Filtra resultados que realmente mencionam IFMS no título ou resumo
        
        Returns:
            Resultados filtrados
        """
        keywords_lower = [k.lower() for k in SEARCH_KEYWORDS]
        filtered = []
        
        for result in self.results:
            titulo_lower = result['titulo'].lower()
            resumo_lower = result['resumo'].lower()
            orgao_lower = result['orgao'].lower()
            
            # Verifica se alguma palavra-chave está presente
            if any(keyword in titulo_lower or 
                   keyword in resumo_lower or 
                   keyword in orgao_lower 
                   for keyword in keywords_lower):
                filtered.append(result)
        
        logger.info(f"Resultados após filtragem: {len(filtered)}")
        self.results = filtered
        return filtered
    
    def export_to_json(self, filename: str = 'results.json'):
        """
        Exporta resultados para JSON
        
        Args:
            filename: Nome do arquivo de saída
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            logger.info(f"Resultados exportados para {filename}")
        except Exception as e:
            logger.error(f"Erro ao exportar para JSON: {e}")


if __name__ == "__main__":
    # Teste básico
    scraper = DOUScraper()
    resultados = scraper.scrape_all_keywords()
    resultados_filtrados = scraper.filter_by_content_keywords()
    
    if resultados_filtrados:
        print(f"\n✓ Encontrados {len(resultados_filtrados)} resultados!")
        for i, resultado in enumerate(resultados_filtrados[:5], 1):
            print(f"\n{i}. {resultado['titulo']}")
            print(f"   Data: {resultado['data_publicacao']}")
            print(f"   URL: {resultado['url']}")
    else:
        print("Nenhum resultado encontrado")
