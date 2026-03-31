"""
Script principal que orquestra o scraping e salva os resultados no repositório
"""

import logging
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.dou_scraper import DOUScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def export_to_markdown(resultados: list, filepath: str):
    """
    Exporta os resultados para um arquivo Markdown bem formatado
    """
    hoje = datetime.now()
    data_formatada = hoje.strftime("%d/%m/%Y às %H:%M")
    data_titulo = hoje.strftime("%d/%m/%Y")

    linhas = [
        f"# DOU — IFMS | {data_titulo}",
        f"",
        f"> Atualizado automaticamente em {data_formatada} (UTC)  ",
        f"> **{len(resultados)} publicação(ões) encontrada(s)**",
        f"",
        f"---",
        f"",
    ]

    if not resultados:
        linhas.append("_Nenhuma publicação encontrada para hoje._")
    else:
        for i, item in enumerate(resultados, 1):
            titulo = item.get('titulo', 'Sem título')
            data_pub = item.get('data_publicacao', '—')
            secao = item.get('secao', '—')
            pagina = item.get('pagina', '—')
            orgao = item.get('orgao', '—')
            resumo = item.get('resumo', '')
            url = item.get('url', '')

            linhas += [
                f"## {i}. {titulo}",
                f"",
                f"| Campo | Valor |",
                f"|-------|-------|",
                f"| **Data de publicação** | {data_pub} |",
                f"| **Seção** | {secao} |",
                f"| **Página** | {pagina} |",
                f"| **Órgão** | {orgao} |",
            ]

            if url:
                linhas.append(f"| **Link** | [Ver publicação no DOU]({url}) |")

            if resumo:
                linhas += [
                    f"",
                    f"> {resumo}",
                ]

            linhas += [f"", f"---", f""]

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas))

    logger.info(f"Arquivo Markdown salvo em: {filepath}")


def update_index(resultados_dir: str):
    """
    Atualiza o README.md dentro da pasta resultados com links para todos os arquivos
    """
    arquivos = sorted(
        [f for f in os.listdir(resultados_dir) if f.endswith('.md') and f != 'README.md'],
        reverse=True
    )

    linhas = [
        "# Resultados — DOU IFMS",
        "",
        "Publicações do Diário Oficial da União relacionadas ao IFMS, coletadas automaticamente.",
        "",
        "| Data | Arquivo |",
        "|------|---------|",
    ]

    for arquivo in arquivos:
        data = arquivo.replace('.md', '')
        linhas.append(f"| {data} | [Ver resultados]({arquivo}) |")

    with open(os.path.join(resultados_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas))

    logger.info("Índice de resultados atualizado")


def main():
    logger.info("=" * 60)
    logger.info("Iniciando DOU Scraper — Instituto Federal de Mato Grosso do Sul")
    logger.info("=" * 60)

    try:
        logger.info("\n[1/3] Iniciando scraping do DOU...")
        scraper = DOUScraper()
        resultados = scraper.scrape_all_keywords()
        logger.info(f"✓ {len(resultados)} resultados encontrados")

        logger.info("\n[2/3] Filtrando resultados...")
        resultados_filtrados = scraper.filter_by_content_keywords()
        logger.info(f"✓ {len(resultados_filtrados)} resultados após filtro")

        logger.info("\n[3/3] Salvando resultados no repositório...")
        hoje = datetime.now().strftime("%Y-%m-%d")
        resultados_dir = "resultados"
        filepath = os.path.join(resultados_dir, f"{hoje}.md")

        export_to_markdown(resultados_filtrados, filepath)
        update_index(resultados_dir)

        logger.info("\n" + "=" * 60)
        logger.info("RESUMO DA EXECUÇÃO")
        logger.info("=" * 60)
        logger.info(f"Resultados encontrados:   {len(resultados)}")
        logger.info(f"Resultados após filtro:   {len(resultados_filtrados)}")
        logger.info(f"Arquivo gerado:           {filepath}")
        logger.info("=" * 60 + "\n")

        return True

    except Exception as e:
        logger.error(f"Erro durante execução: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
