"""
Script principal — DOU Scraper IFMS
Modos: daily (padrão), weekly, backfill
"""

import argparse
import logging
import sys
import os
from datetime import datetime, date, timedelta

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

RESULTADOS_DIR = 'resultados'
SEMANAS_DIR = os.path.join(RESULTADOS_DIR, 'semanas')


# ---------------------------------------------------------------------------
# Exportação diária
# ---------------------------------------------------------------------------

def export_daily_markdown(resultados: list, ref_date: date) -> str:
    data_fmt = ref_date.strftime('%d/%m/%Y')
    filepath = os.path.join(RESULTADOS_DIR, f"{ref_date.isoformat()}.md")

    linhas = [
        f"# DOU — IFMS | {data_fmt}",
        f"",
        f"> Coletado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} (UTC)  ",
        f"> **{len(resultados)} publicação(ões) encontrada(s)**",
        f"",
        f"---",
        f"",
    ]

    if not resultados:
        linhas.append("_Nenhuma publicação encontrada._")
    else:
        for i, item in enumerate(resultados, 1):
            linhas += _format_item(i, item)

    os.makedirs(RESULTADOS_DIR, exist_ok=True)
    _write(filepath, linhas)
    return filepath


# ---------------------------------------------------------------------------
# Exportação semanal
# ---------------------------------------------------------------------------

def export_weekly_markdown(resultados: list, start: date, end: date) -> str:
    os.makedirs(SEMANAS_DIR, exist_ok=True)
    filename = f"{start.isoformat()}_{end.isoformat()}.md"
    filepath = os.path.join(SEMANAS_DIR, filename)

    # Agrupa por dia
    by_day: dict = {}
    for item in resultados:
        pub = item.get('data_publicacao', '')
        from src.dou_scraper import _parse_date
        d = _parse_date(pub)
        key = d.isoformat() if d else 'data desconhecida'
        by_day.setdefault(key, []).append(item)

    semana_fmt = f"{start.strftime('%d/%m')} a {end.strftime('%d/%m/%Y')}"
    linhas = [
        f"# DOU — IFMS | Semana {semana_fmt}",
        f"",
        f"> Coletado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} (UTC)  ",
        f"> **{len(resultados)} publicação(ões) encontrada(s) na semana**",
        f"",
        f"---",
        f"",
    ]

    if not resultados:
        linhas.append("_Nenhuma publicação encontrada na semana._")
    else:
        DIAS_PT = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira',
                   3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}

        for key in sorted(by_day.keys()):
            itens = by_day[key]
            try:
                d = date.fromisoformat(key)
                dia_nome = DIAS_PT.get(d.weekday(), '')
                titulo_dia = f"## {dia_nome}, {d.strftime('%d/%m/%Y')}  ({len(itens)} publicação(ões))"
            except ValueError:
                titulo_dia = f"## {key}"

            linhas += [titulo_dia, ""]
            for i, item in enumerate(itens, 1):
                linhas += _format_item(i, item)

    _write(filepath, linhas)
    return filepath


# ---------------------------------------------------------------------------
# Índice
# ---------------------------------------------------------------------------

def update_index(ultimos_resultados: list = None, ultimo_periodo: str = ''):
    os.makedirs(RESULTADOS_DIR, exist_ok=True)

    diarios = sorted(
        [f for f in os.listdir(RESULTADOS_DIR)
         if f.endswith('.md') and f != 'README.md' and '_' not in f],
        reverse=True
    )

    semanais = []
    if os.path.exists(SEMANAS_DIR):
        semanais = sorted(
            [f for f in os.listdir(SEMANAS_DIR) if f.endswith('.md') and f != 'README.md'],
            reverse=True
        )

    agora = datetime.now().strftime('%d/%m/%Y às %H:%M')
    total = len(ultimos_resultados) if ultimos_resultados else 0

    linhas = [
        "# DOU — IFMS | Publicações Monitoradas",
        "",
        f"Atualizado em {agora} UTC  ",
        f"Coleta automática do Diário Oficial da União — Segunda a Sexta",
        "",
        "---",
        "",
    ]

    # Mostra publicações recentes diretamente no README
    if ultimos_resultados:
        linhas += [
            f"## Publicações recentes — {ultimo_periodo}",
            f"**{total} publicação(ões) encontrada(s)**",
            "",
        ]
        for i, item in enumerate(ultimos_resultados, 1):
            linhas += _format_item(i, item)
    else:
        linhas += [
            f"## Publicações recentes — {ultimo_periodo}",
            "_Nenhuma publicação encontrada no período._",
            "",
            "---",
            "",
        ]

    # Histórico
    if semanais or diarios:
        linhas += ["## Histórico", ""]

    if semanais:
        linhas += ["**Relatórios Semanais**", ""]
        for f in semanais:
            partes = f.replace('.md', '').split('_')
            if len(partes) == 2:
                d1 = _fmt_date(partes[0])
                d2 = _fmt_date(partes[1])
                label = f"{d1} → {d2}"
            else:
                label = f
            linhas.append(f"- [{label}](semanas/{f})")
        linhas.append("")

    if diarios:
        linhas += ["**Dias anteriores**", ""]
        for f in diarios:
            d = _fmt_date(f.replace('.md', ''))
            linhas.append(f"- [{d}]({f})")

    _write(os.path.join(RESULTADOS_DIR, 'README.md'), linhas)
    logger.info("Índice atualizado")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fmt_date(value: str) -> str:
    """Converte qualquer formato de data para DD/MM/YYYY."""
    from src.dou_scraper import _parse_date
    d = _parse_date(value)
    return d.strftime('%d/%m/%Y') if d else (value or '—')


def _fmt_secao(value: str) -> str:
    """Normaliza seção: DO1/do1 → Seção 1."""
    mapping = {'DO1': 'Seção 1', 'DO2': 'Seção 2', 'DO3': 'Seção 3',
               'do1': 'Seção 1', 'do2': 'Seção 2', 'do3': 'Seção 3'}
    return mapping.get(value, value or '—')


def _format_item(i: int, item: dict) -> list:
    titulo = item.get('titulo', 'Sem título')
    orgao  = item.get('orgao', '—') or '—'
    data   = _fmt_date(item.get('data_publicacao', ''))
    secao  = _fmt_secao(item.get('secao', ''))
    pagina = item.get('pagina', '') or ''
    url    = item.get('url', '')
    resumo = item.get('resumo', '') or ''

    meta = f"**Data:** {data} | **{secao}**"
    if pagina:
        meta += f" | **Página:** {pagina}"

    linhas = [
        f"### {i}. {titulo}",
        f"",
        f"**Órgão:** {orgao}  ",
        meta + "  ",
    ]
    if url:
        linhas.append(f"**Link:** [Ver publicação completa no DOU]({url})")
    if resumo:
        linhas += ["", f"> {resumo}"]
    linhas += ["", "---", ""]
    return linhas


def _write(filepath: str, linhas: list):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas))
    logger.info(f"Salvo: {filepath}")


def _run_scraper(start_date: date = None, end_date: date = None) -> list:
    scraper = DOUScraper()
    resultados = scraper.scrape_all_keywords(start_date=start_date, end_date=end_date)
    resultados = scraper.filter_by_content_keywords()
    if start_date and end_date:
        resultados = scraper.filter_by_date_range(start_date, end_date)
    return resultados


# ---------------------------------------------------------------------------
# Modos de execução
# ---------------------------------------------------------------------------

def run_daily():
    logger.info("=== MODO: DIÁRIO ===")
    hoje = date.today()
    resultados = _run_scraper(start_date=hoje, end_date=hoje)
    filepath = export_daily_markdown(resultados, hoje)
    update_index(resultados, hoje.strftime('%d/%m/%Y'))
    logger.info(f"Concluído: {filepath} | {len(resultados)} resultado(s)")
    return True


def run_weekly():
    logger.info("=== MODO: SEMANAL ===")
    hoje = date.today()
    # Segunda-feira da semana passada
    segunda = hoje - timedelta(days=hoje.weekday() + 7)
    sexta = segunda + timedelta(days=4)
    return run_range(segunda, sexta, weekly_report=True)



def run_range(start: date, end: date, weekly_report: bool = True):
    logger.info(f"=== MODO: BACKFILL | {start} → {end} ===")
    resultados = _run_scraper(start_date=start, end_date=end)

    from src.dou_scraper import _parse_date

    # Gera arquivos diários para cada dia do intervalo
    current = start
    while current <= end:
        dia_resultados = [
            r for r in resultados
            if _parse_date(r.get('data_publicacao', '')) == current
        ]
        export_daily_markdown(dia_resultados, current)
        current += timedelta(days=1)

    # Gera relatório semanal
    periodo = f"{start.strftime('%d/%m')} a {end.strftime('%d/%m/%Y')}"
    if weekly_report:
        filepath = export_weekly_markdown(resultados, start, end)
        logger.info(f"Relatório semanal: {filepath}")

    update_index(resultados, periodo)
    logger.info(f"Concluído: {len(resultados)} resultado(s) no período")
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='DOU Scraper IFMS')
    parser.add_argument('--mode', choices=['daily', 'weekly', 'backfill'],
                        default='daily', help='Modo de execução')
    parser.add_argument('--start', help='Data inicial YYYY-MM-DD (backfill)')
    parser.add_argument('--end', help='Data final YYYY-MM-DD (backfill)')
    args = parser.parse_args()

    try:
        if args.mode == 'daily':
            return run_daily()

        elif args.mode == 'weekly':
            return run_weekly()

        elif args.mode == 'backfill':
            if not args.start or not args.end:
                logger.error("--start e --end são obrigatórios no modo backfill")
                return False
            start = date.fromisoformat(args.start)
            end = date.fromisoformat(args.end)
            return run_range(start, end)

    except Exception as e:
        logger.error(f"Erro: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
