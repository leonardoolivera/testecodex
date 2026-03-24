"""
Script principal que orquestra o scraping e exportação para Google Sheets
"""

import logging
import sys
import os
from datetime import datetime

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.dou_scraper import DOUScraper
from src.google_sheets import GoogleSheetsIntegration
from config.config import SPREADSHEET_ID

# Configurar logging com mais detalhes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """
    Função principal que coordena todo o processo
    """
    logger.info("=" * 60)
    logger.info("Iniciando DOU Scraper - Instituto Federal de Mato Grosso do Sul")
    logger.info("=" * 60)
    
    try:
        # Passo 1: Faz o scraping
        logger.info("\n[1/4] Iniciando scraping do DOU...")
        scraper = DOUScraper()
        resultados = scraper.scrape_all_keywords()
        logger.info(f"✓ {len(resultados)} resultados encontrados")
        
        # Passo 2: Filtra os resultados
        logger.info("\n[2/4] Filtrando resultados...")
        resultados_filtrados = scraper.filter_by_content_keywords()
        logger.info(f"✓ {len(resultados_filtrados)} resultados após filtro")
        
        if not resultados_filtrados:
            logger.warning("Nenhum resultado encontrado após filtros")
            return False
        
        # Passo 3: Exporta para JSON (backup)
        logger.info("\n[3/4] Salvando backup em JSON...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = f"resultados_dou_{timestamp}.json"
        scraper.export_to_json(json_file)
        logger.info(f"✓ Backup salvo em: {json_file}")
        
        # Passo 4: Exporta para Google Sheets
        logger.info("\n[4/4] Exportando para Google Sheets...")
        
        if not SPREADSHEET_ID:
            logger.error("SPREADSHEET_ID não configurado!")
            logger.error("Por favor, siga as instruções no README.md")
            return False
        
        sheets = GoogleSheetsIntegration()
        
        # Verifica se a planilha existe
        if not sheets.check_spreadsheet_exists():
            logger.error(f"Planilha ID {SPREADSHEET_ID} não encontrada!")
            logger.error("Verifique se o ID está correto e se você tem acesso")
            return False
        
        # Adiciona dados à planilha
        sheets.add_headers()
        sheets.append_rows(resultados_filtrados)
        
        url = sheets.get_spreadsheet_url()
        logger.info(f"✓ Dados exportados com sucesso!")
        logger.info(f"✓ Acesse a planilha: {url}")
        
        # Resumo final
        logger.info("\n" + "=" * 60)
        logger.info("RESUMO DA EXECUÇÃO")
        logger.info("=" * 60)
        logger.info(f"Resultados encontrados: {len(resultados)}")
        logger.info(f"Resultados após filtro: {len(resultados_filtrados)}")
        logger.info(f"Linhas adicionadas: {len(resultados_filtrados)}")
        logger.info(f"Arquivo JSON: {json_file}")
        logger.info(f"Planilha: {url}")
        logger.info("=" * 60 + "\n")
        
        return True
        
    except FileNotFoundError as e:
        logger.error(f"Erro de arquivo: {e}")
        logger.error("Verifique se as credenciais do Google foram configuradas")
        return False
    except Exception as e:
        logger.error(f"Erro durante execução: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
