# DOU Scraper — IFMS

Coleta automaticamente publicações do Diário Oficial da União relacionadas ao IFMS e salva os resultados diretamente neste repositório.

---

## Ver os resultados

Acesse a pasta **[resultados/](resultados/)** neste repositório.

- Cada arquivo `YYYY-MM-DD.md` contém as publicações do dia
- A pasta `resultados/semanas/` contém os relatórios semanais
- O arquivo `resultados/README.md` lista tudo com links diretos

---

## Execução automática

O scraper roda automaticamente:

| Quando | O que faz |
|--------|-----------|
| Segunda a sexta, 06:00 (Brasília) | Coleta publicações do dia |
| Toda segunda-feira | Gera relatório da semana anterior |

---

## Rodar manualmente

1. Acesse **Actions** no repositório
2. Clique em **DOU Scraper - IFMS**
3. Clique em **Run workflow**
4. Escolha o modo:

| Modo | Quando usar |
|------|-------------|
| `daily` | Coleta de hoje |
| `weekly` | Relatório da semana passada |
| `backfill` | Período específico — preencha **Data inicial** e **Data final** no formato `YYYY-MM-DD` |

---

## Primeira configuração

Nenhuma configuração necessária. Basta ter o repositório no GitHub e o workflow já funciona.
