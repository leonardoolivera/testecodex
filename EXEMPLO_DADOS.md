# Exemplo de resultado do DOU Scraper

Este arquivo mostra a estrutura dos dados coletados.

## JSON Example (resultados_dou_YYYYMMDD_HHMMSS.json)

```json
[
  {
    "data_publicacao": "2026-03-24",
    "titulo": "EDITAL nº 123/2026 - Instituto Federal de Mato Grosso do Sul",
    "secao": "3",
    "pagina": "45",
    "url": "https://www.in.gov.br/web/dou/-/edital-123-2026...",
    "orgao": "Instituto Federal de Mato Grosso do Sul",
    "resumo": "Abre inscrições para posição de docentes em Engenharia de Software...",
    "data_coleta": "2026-03-24T10:30:45.123456"
  },
  {
    "data_publicacao": "2026-03-20",
    "titulo": "PORTARIA nº 456/2026 - IFMS",
    "secao": "2",
    "pagina": "32",
    "url": "https://www.in.gov.br/web/dou/-/portaria-456-2026...",
    "orgao": "Instituto Federal de Mato Grosso do Sul",
    "resumo": "Dispõe sobre reorganização administrativa dos campus...",
    "data_coleta": "2026-03-24T10:30:50.654321"
  }
]
```

## Google Sheets Format

Na planilha Google Sheets, os dados aparecem assim:

| Data de Publicação | Título | Seção | Página | URL | Resumo | Data de Coleta |
|---|---|---|---|---|---|---|
| 2026-03-24 | EDITAL nº 123/2026 - Instituto Federal de Mato Grosso do Sul | 3 | 45 | https://ww... | Abre inscrições para posição de docentes em... | 2026-03-24T10:30:45 |
| 2026-03-20 | PORTARIA nº 456/2026 - IFMS | 2 | 32 | https://ww... | Dispõe sobre reorganização administrativa... | 2026-03-24T10:30:50 |

## Campos

- **Data de Publicação**: Data em que a publicação foi publicada no DOU
- **Título**: Título completo da publicação 
- **Seção**: Seção do DOU (1, 2, 3, etc)
- **Página**: Número da página na edição
- **URL**: Link direto para a publicação no DOU
- **Resumo**: Ementa/resumo da publicação (primeiros 200 caracteres)
- **Data de Coleta**: Data e hora em que o dado foi extraído
