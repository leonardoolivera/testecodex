"""
Testes básicos para o DOU Scraper
Execute com: pytest tests/
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.dou_scraper import DOUScraper
from config.config import SHEET_COLUMNS


class TestDOUScraper(unittest.TestCase):
    """
    Testes para a classe DOUScraper
    """
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.scraper = DOUScraper()
    
    def test_scraper_initialization(self):
        """Testa se o scraper inicializa corretamente"""
        self.assertIsNotNone(self.scraper.session)
        self.assertEqual(len(self.scraper.results), 0)
    
    def test_parse_document_valid(self):
        """Testa parsing de um documento válido"""
        doc = {
            'titulo': 'Teste Edital',
            'secao': '1',
            'pagina': 10,
            'data_publicacao': '2026-03-24',
            'url': 'https://example.com/test',
            'orgao': 'IFMS',
            'ementa': 'Resumo do teste'
        }
        
        result = self.scraper._parse_document(doc)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['titulo'], 'Teste Edital')
        self.assertEqual(result['url'], 'https://example.com/test')
    
    def test_parse_document_invalid(self):
        """Testa parsing de um documento inválido (sem título)"""
        doc = {
            'titulo': '',
            'url': 'https://example.com/test'
        }
        
        result = self.scraper._parse_document(doc)
        
        self.assertIsNone(result)
    
    def test_filter_by_keywords(self):
        """Testa filtro por palavras-chave"""
        # Adiciona dados de teste
        self.scraper.results = [
            {
                'titulo': 'IFMS - Instituto Federal',
                'resumo': 'Publicação importante',
                'orgao': 'Instituto Federal de Mato Grosso do Sul',
                'url': 'https://example1.com'
            },
            {
                'titulo': 'Outra instituição',
                'resumo': 'Não relevante',
                'orgao': 'Outro órgão',
                'url': 'https://example2.com'
            }
        ]
        
        filtered = self.scraper.filter_by_content_keywords()
        
        self.assertEqual(len(filtered), 1)
        self.assertIn('IFMS', filtered[0]['titulo'])


class TestConfig(unittest.TestCase):
    """
    Testes para configuração
    """
    
    def test_sheet_columns_exist(self):
        """Testa se as colunas da planilha estão configuradas"""
        self.assertIsNotNone(SHEET_COLUMNS)
        self.assertGreater(len(SHEET_COLUMNS), 0)
        self.assertIn("Data de Publicação", SHEET_COLUMNS)
        self.assertIn("Título", SHEET_COLUMNS)
        self.assertIn("URL", SHEET_COLUMNS)


if __name__ == '__main__':
    unittest.main()
