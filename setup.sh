#!/bin/bash

# Script de instalação automática do DOU Scraper

set -e

echo "================================="
echo "DOU Scraper - Setup Automático"
echo "================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 não encontrado. Por favor instale Python 3.8+${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 encontrado$(python3 --version)${NC}"
echo ""

# Cria ambiente virtual
echo "Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Ambiente virtual criado${NC}"
else
    echo -e "${YELLOW}! Ambiente virtual já existe${NC}"
fi

# Ativa ambiente virtual
source venv/bin/activate

# Instala dependências
echo ""
echo "Instalando dependências..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependências instaladas${NC}"

# Cria diretório de credenciais se não existe
if [ ! -d "credentials" ]; then
    mkdir -p credentials
    echo -e "${GREEN}✓ Diretório credentials/ criado${NC}"
fi

# Instrões finais
echo ""
echo "================================="
echo "Setup Concluído com Sucesso! ✓"
echo "================================="
echo ""
echo "Próximos passos:"
echo ""
echo "1. IMPORTANTE: Configure Google Sheets"
echo "   - Leia o arquivo: SETUP_GUIA.md"
echo "   - Ou comece rápido: QUICKSTART.md"
echo ""
echo "2. Baixe credenciais OAuth do Google Cloud"
echo "   - Salve como: credentials/credentials.json"
echo ""
echo "3. Crie uma planilha no Google Sheets"
echo "   - Nome: 'DOU - IFMS'"
echo "   - Copie o ID da URL"
echo ""
echo "4. Configure config/config.py"
echo "   - SPREADSHEET_ID = 'seu_id_aqui'"
echo ""
echo "5. Execute:"
echo "   source venv/bin/activate  # Se necessário"
echo "   python main.py"
echo ""
echo "================================="
echo ""
echo "Precisa de ajuda?"
echo "- Leia: README.md"
echo "- Leia: SETUP_GUIA.md"
echo "- Teste: python exemplos.py"
echo ""
