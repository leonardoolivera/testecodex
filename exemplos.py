"""
Script de exemplo para uso avançado do DOU Scraper

Este arquivo mostra como usar as classes principais de forma individual
para ter mais controle sobre o processo.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.dou_scraper import DOUScraper
from src.google_sheets import GoogleSheetsIntegration
from config.config import SPREADSHEET_ID


def exemplo_1_scraping_basico():
    """
    Exemplo 1: Fazer scraping básico do DOU
    """
    print("=" * 60)
    print("EXEMPLO 1: Scraping Básico")
    print("=" * 60)
    
    scraper = DOUScraper()
    
    # Busca por uma palavra-chave específica
    resultados = scraper.search_dou("Instituto Federal de Mato Grosso do Sul", pages=2)
    
    print(f"\n✓ Encontrados {len(resultados)} resultados")
    print("\nPrimeiros 3 resultados:")
    for i, resultado in enumerate(resultados[:3], 1):
        print(f"\n{i}. {resultado['titulo']}")
        print(f"   Data: {resultado['data_publicacao']}")
        print(f"   URL: {resultado['url']}")


def exemplo_2_scraping_multiplas_keywords():
    """
    Exemplo 2: Buscar com múltiplas palavras-chave
    """
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Múltiplas Palavras-chave")
    print("=" * 60)
    
    scraper = DOUScraper()
    
    # Busca com todas as palavras-chave configuradas
    resultados = scraper.scrape_all_keywords()
    
    print(f"\n✓ Total encontrados: {len(resultados)}")
    
    # Filtra por conteúdo
    resultados_filtrados = scraper.filter_by_content_keywords()
    
    print(f"✓ Após filtro: {len(resultados_filtrados)}")


def exemplo_3_exportar_json():
    """
    Exemplo 3: Fazer scraping e salvar em JSON
    """
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Exportar para JSON")
    print("=" * 60)
    
    scraper = DOUScraper()
    
    # Faz o scraping
    resultados = scraper.scrape_all_keywords()
    resultados_filtrados = scraper.filter_by_content_keywords()
    
    # Exporta para JSON com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo = f"meus_resultados_{timestamp}.json"
    
    scraper.export_to_json(arquivo)
    
    print(f"\n✓ {len(resultados_filtrados)} resultados salvos em: {arquivo}")
    print("\nVocê pode abrir o arquivo JSON em um editor de texto")


def exemplo_4_importar_para_sheets():
    """
    Exemplo 4: Importar dados do JSON para Google Sheets
    """
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Importar para Google Sheets")
    print("=" * 60)
    
    if not SPREADSHEET_ID:
        print("❌ SPREADSHEET_ID não configurado!")
        print("   Configure em config/config.py")
        return
    
    # Faz o scraping
    scraper = DOUScraper()
    resultados = scraper.scrape_all_keywords()
    resultados_filtrados = scraper.filter_by_content_keywords()
    
    if not resultados_filtrados:
        print("❌ Nenhum resultado para exportar")
        return
    
    # Conecta ao Google Sheets
    sheets = GoogleSheetsIntegration()
    
    # Adiciona headers
    sheets.add_headers()
    
    # Adiciona dados
    sheets.append_rows(resultados_filtrados)
    
    url = sheets.get_spreadsheet_url()
    
    print(f"\n✓ {len(resultados_filtrados)} linhas adicionadas")
    print(f"✓ Acesse: {url}")


def exemplo_5_dados_customizados():
    """
    Exemplo 5: Adicionar dados customizados à planilha
    """
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Dados Customizados")
    print("=" * 60)
    
    if not SPREADSHEET_ID:
        print("❌ SPREADSHEET_ID não configurado!")
        return
    
    sheets = GoogleSheetsIntegration()
    
    # Cria dados manualmente
    dados_customizados = [
        {
            'data_publicacao': '2026-03-24',
            'titulo': 'Exemplo Manual 1',
            'secao': '2',
            'pagina': '42',
            'url': 'https://example.com/1',
            'resumo': 'Este é um resumo de exemplo',
            'data_coleta': datetime.now().isoformat()
        },
        {
            'data_publicacao': '2026-03-23',
            'titulo': 'Exemplo Manual 2',
            'secao': '3',
            'pagina': '85',
            'url': 'https://example.com/2',
            'resumo': 'Outro resumo de teste',
            'data_coleta': datetime.now().isoformat()
        }
    ]
    
    # Adiciona à planilha
    sheets.add_headers()
    sheets.append_rows(dados_customizados)
    
    print(f"\n✓ {len(dados_customizados)} linhas de exemplo adicionadas")
    print(f"✓ URL: {sheets.get_spreadsheet_url()}")


def main():
    """
    Menu principal
    """
    print("\n" + "=" * 60)
    print("DOU SCRAPER - Exemplos de Uso")
    print("=" * 60)
    print("\n1. Scraping Básico")
    print("2. Scraping com Múltiplas Palavras-chave")
    print("3. Exportar para JSON")
    print("4. Importar para Google Sheets")
    print("5. Adicionar Dados Customizados")
    print("0. Sair")
    print()
    
    opcao = input("Escolha uma opção (0-5): ").strip()
    
    if opcao == "1":
        exemplo_1_scraping_basico()
    elif opcao == "2":
        exemplo_2_scraping_multiplas_keywords()
    elif opcao == "3":
        exemplo_3_exportar_json()
    elif opcao == "4":
        exemplo_4_importar_para_sheets()
    elif opcao == "5":
        exemplo_5_dados_customizados()
    elif opcao == "0":
        print("Até logo!")
        return
    else:
        print("❌ Opção inválida")
        return
    
    input("\nPressione ENTER para voltar ao menu...")
    main()


if __name__ == "__main__":
    main()
