"""
Configurações do Scraper DOU
"""

# URLs do Diário Oficial da União
DOU_BASE_URL = "https://www.in.gov.br/consulta/-/asearch"
DOU_API_URL = "https://www.in.gov.br/api/asearch"

# Palavras-chave para busca
SEARCH_KEYWORDS = [
    "IFMS",
    "Instituto Federal de Educação, Ciência e Tecnologia de Mato Grosso do Sul",
    "Instituto Federal de Mato Grosso do Sul",
]

# Configurações de Google Sheets
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GOOGLE_CREDENTIALS_FILE = 'credentials/credentials.json'
GOOGLE_TOKEN_FILE = 'credentials/token.pickle'

# ID da planilha Google Sheets (adicionar após criar)
# Você pode obter isso da URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
SPREADSHEET_ID = None  # Será setado no README

# Nome da aba (sheet)
SHEET_NAME = "DOU - IFMS"

# Configurações de busca
SEARCH_LIMIT = 100  # Número máximo de resultados por busca
SORT_BY = "publicacao"  # Campo para ordenação
ORDER = "desc"  # Ordem decrescente (mais recentes primeiro)

# Configurações de processamento
MIN_CONTENT_LENGTH = 50  # Tamanho mínimo do conteúdo para validar
TIMEOUT = 10  # Timeout em segundos para requisições

# Campos da planilha
SHEET_COLUMNS = [
    "Data de Publicação",
    "Título",
    "Seção",
    "Página",
    "URL",
    "Resumo",
    "Data de Coleta"
]
