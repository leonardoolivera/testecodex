# 🏗️ Arquitetura do DOU Scraper

## 📊 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOU Scraper - Fluxo Completo                 │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  main.py         │  ← PONTO DE ENTRADA
│   (orquestrador) │     Execute este arquivo
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│  1️⃣  SCRAPING DO DOU                              │
│  ┌──────────────────────────────────────────┐   │
│  │ DOUScraper.search_dou()                  │   │
│  │ - Acessa API do DOU                      │   │
│  │ - Busca por palavras-chave               │   │
│  │ - Faz 5 requisições (5 páginas)          │   │
│  │ - Extrai: titulo, url, data, etc         │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  Usa: requests, json, logging                   │
│  Resultado: ~50-100 documentos                  │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  2️⃣  FILTRAGEM E VALIDAÇÃO                        │
│  ┌──────────────────────────────────────────┐   │
│  │ DOUScraper.filter_by_content_keywords()  │   │
│  │ - Verifica presença de "IFMS"            │   │
│  │ - Valida tamanho mínimo de conteúdo      │   │
│  │ - Remove duplicatas                      │   │
│  │ - Organiza por data                      │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  Usa: string matching, deduplication             │
│  Resultado: ~10-30 documentos relevantes        │
└──────────────────┬───────────────────────────────┘
                   │
                   ├─────────────────────────────────────┐
                   │                                     │
                   ▼                                     ▼
    ┌──────────────────────────┐      ┌──────────────────────────┐
    │  3️⃣  BACKUP JSON            │      │  3️⃣  EXPORTAR SHEETS      │
    │  ┌────────────────────┐   │      │  ┌────────────────────┐ │
    │  │ export_to_json()   │   │      │  │GoogleSheetsIntegr()│ │
    │  │ - Salva arquivo    │   │      │  │ ────────────────── │ │
    │  │ resultados_dou_... │   │      │  │ 1. Autentica      │ │
    │  │   _YYYYMMDD_HMM... │   │      │  │ 2. Adiciona headers│ │
    │  │ - Preserva dados   │   │      │  │ 3. Exporta dados  │ │
    │  │ - Histórico        │   │      │  │ 4. Formata células│ │
    │  └────────────────────┘   │      │  └────────────────────┘ │
    │                            │      │                         │
    │ Usa: JSON, datetime        │      │ Usa: Google API, OAuth  │
    │ Resultado: arquivo JSON    │      │ Resultado: planilha     │
    └──────────────────────────┘      └──────────────────────────┘
                   │                                     │
                   └─────────────────────────────────────┘
                            │
                            ▼
              ┌──────────────────────────────┐
              │  ✅ SUCESSO!                 │
              │  ────────────────────────    │
              │  - JSON salvo               │
              │  - Google Sheets atualizado │
              │  - Logs gerados             │
              │  - Relatório exibido        │
              └──────────────────────────────┘
```

## 📁 Estrutura de Módulos

```
main.py (orquestrador principal)
│
├─→ config/config.py (configurações)
│   ├─ URLs do DOU
│   ├─ Palavras-chave
│   ├─ Credenciais Google
│   └─ Estrutura de dados
│
├─→ src/dou_scraper.py (web scraper)
│   ├─ DOUScraper (classe)
│   │   ├─ search_dou() - busca por termo
│   │   ├─ scrape_all_keywords() - busca tudo
│   │   ├─ filter_by_content_keywords() - filtra
│   │   ├─ _parse_document() - extrai dados
│   │   └─ export_to_json() - salva JSON
│   └─ Usa: requests, BeautifulSoup, json
│
└─→ src/google_sheets.py (integração)
    ├─ GoogleSheetsIntegration (classe)
    │   ├─ authenticate() - faz login Google
    │   ├─ create_spreadsheet() - cria planilha
    │   ├─ add_headers() - adiciona colunas
    │   ├─ append_rows() - adiciona dados
    │   ├─ _format_headers() - formata células
    │   └─ get_spreadsheet_url() - URL
    └─ Usa: Google Auth, Sheets API
```

## 🔄 Ciclo de Vida

### Primeira Execução
```
1. main.py iniciado
2. DOUScraper criado
3. Busca no DOU por todas as keywords
4. Filtra resultados
5. Salva JSON
6. Tenta autenticar Google
   ├─ Credenciais não existem?
   │  └─ Navegador abre para login
   ├─ Faz login
   └─ Token armazenado em credentials/token.pickle
7. Exporta para Google Sheets
8. Mostra URL da planilha
9. FIM
```

### Execuções Subsequentes
```
1. main.py iniciado
2. DOUScraper criado
3. Busca no DOU por todas as keywords
4. Filtra resultados
5. Salva JSON
6. Token.pickle carregado (login rápido)
7. Exporta para Google Sheets
8. Mostra URL da planilha
9. FIM
```

## 🔐 Fluxo de Autenticação Google

```
┌─────────────────────────────────────┐
│ Primeira Execução                   │
└────────────┬────────────────────────┘
             │
             ▼
    ┌─────────────────────┐
    │ Procura token.pickle│
    └────────────┬────────┘
                 │
        ┌────────┴────────┐
        │ NÃO EXISTE?     │
        └────────┬────────┘
                 │
        SIM ─────┼───── NÃO
        │        │      │
        ▼        │      ▼
   ┌───────┐   │   ┌──────────┐
   │ Token │   │   │ Valido?  │
   │ novo  │   │   └────┬─────┘
   └────┬──┘   │   SIM  │ NÃO
        │      │   │    ▼
        ▼      │   │   ┌──────────┐
   ┌──────┐    │   │   │ Refresh? │
   │OAuth │    │   │   └────┬─────┘
   │Flow  │    │   │   SIM  │ NÃO
   └────┬─┘    │   │   │    ▼
        │      │   │   │   ┌──────────┐
        ▼      │   │   └──→│ Novo    │
   ┌──────┐    │   │       │ OAuth   │
   │Token │    │   │       │ Flow    │
   │salvo │    │   │       └────┬────┘
   └──────┘    │   │            │
              │   │        ┌────▼──────┐
              └───┼───────→│ Conectado │
                  │        │ ao Google │
                  └────────└───────────┘
```

## 📊 Estrutura de Dados

### Documento Parseado
```python
{
    'data_publicacao': str,     # "2026-03-24"
    'titulo': str,              # "EDITAL nº 123/2026..."
    'secao': str,               # "3"
    'pagina': str,              # "45"
    'url': str,                 # "https://..."
    'orgao': str,               # "IFMS"
    'resumo': str,              # Primeiros 200 chars
    'data_coleta': str          # ISO timestamp
}
```

### Linha da Planilha
```
["2026-03-24", "EDITAL nº...", "3", "45", 
 "https://...", "Resumo...",  "2026-03-24T10:30:45"]
```

## 🚀 Fluxo de Execução Automática

### GitHub Actions
```
Agendamiento: Diariamente às 6 AM UTC
              │
              ▼
        ┌─────────────┐
        │ Cria VM     │
        │ Ubuntu      │
        └──────┬──────┘
               │
               ▼
        ┌──────────────────┐
        │ Setup Python     │
        │ Instala deps     │
        └──────┬───────────┘
               │
               ▼
        ┌──────────────────┐
        │ Restaura creds   │
        │ (do secrets)     │
        └──────┬───────────┘
               │
               ▼
        ┌──────────────────┐
        │ Python main.py   │
        └──────┬───────────┘
               │
               ▼
        ┌──────────────────┐
        │ Salva logs       │
        │ (artifacts)      │
        └──────────────────┘
```

### Docker
```
docker-compose up
      │
      ▼
┌──────────────┐
│ Dockerfile   │
├──────────────┤
│ FROM python  │
│ COPY files   │
│ RUN pip      │
│ CMD main.py  │
└──────────────┘
      │
      ▼
┌──────────────┐
│ Container    │
│ executando   │
└──────────────┘
```

## 🔍 Fluxo de Busca Detalhado

```
Input: Palavra-chave = "IFMS"
│
├─→ Página 1
│  ├─ 10 documentos
│  ├─ Parse cada um
│  └─ Adiciona a results[]
│
├─→ Página 2
│  ├─ 10 documentos
│  ├─ Parse cada um
│  └─ Adiciona a results[]
│
├─→ Página 3-5
│  └─ Mesmo processo
│
├─→ Próximas keywords
│  └─ Repete tudo
│
└─→ Remove duplicatas
   └─ ~30-50 únicos
```

## ⚠️ Tratamento de Erros

```
Erro em requisição HTTP
├─ Registra no log
├─ Continua próxima página
└─ Mostra resumo de erros

Erro no parsing
├─ Registra documento problemático
├─ Pula para próximo
└─ Continua

Erro na autenticação Google
├─ Pede novo login
├─ Salva novo token
└─ Continua

Nenhum resultado
├─ Log de aviso
├─ Salva JSON vazio
└─ Mostra mensagem
```

---

## 📈 Métricas Típicas

| Métrica | Valor Típico |
|---------|-------------|
| Tempo de busca | 30-60s |
| Documentos encontrados | 50-100 |
| Após filtro | 10-30 |
| Tempo de exportação | 5-10s |
| Tempo total | ~1-2 minutos |

---

*Diagrama criado em: 24/03/2026*
