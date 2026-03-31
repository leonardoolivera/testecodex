# Guia Completo de Configuração do DOU Scraper

Este guia passo a passo ajudará você a configurar o scraper do zero.

## Pré-requisitos

- Python 3.8+
- Conta do Google (Gmail, Google Workspace, etc)
- Git (opcional)

## ⚙️ Instalação do Projeto

### 1. Baixar o projeto

```bash
# Com Git
git clone https://github.com/leonardoolivera/testecodex.git
cd testecodex

# Ou baixe manualmente do GitHub
```

### 2. Criar ambiente virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## 🔑 Configuração Google Sheets (Passo mais importante!)

### Etapa 1: Criar projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Clique em "Select a Project" (canto superior esquerdo)
3. Clique em "NEW PROJECT"
4. Nome do projeto: `DOU-Scraper` (ou seu nome preferido)
5. Clique em "Create"
6. Aguarde a criação (pode levar alguns segundos)

### Etapa 2: Baixar credenciais OAuth

1. No Google Cloud Console, abra o projeto criado
2. Vá para "APIs & Services" → "Credentials"
3. Clique em "+ Create Credentials" → "OAuth 2.0 Client ID"
4. Se pedir para configurar "OAuth consent screen":
   - Clique em "Configure Consent Screen"
   - Selecione "External"
   - Preencha os dados (nome do app, email suporte, etc)
   - Salve e continue

5. De volta em "Credentials", clique em "+ Create Credentials" → "OAuth 2.0 Client ID" novamente
6. Selecione "Desktop application"
7. Clique em "Create"
8. Clique no download JSON (ícone de download)

### Etapa 3: Adicionar credenciais ao projeto

1. Localize o arquivo baixado (provavelmente `client_secret_*.json`)
2. Copie para a pasta do projeto:
   ```bash
   mv ~/Downloads/client_secret_*.json ./credentials/credentials.json
   ```

3. Verifique se o arquivo está no lugar certo:
   ```bash
   ls -la credentials/credentials.json
   ```

### Etapa 4: Ativar Google Sheets API

1. No Google Cloud Console
2. Vá para "APIs & Services" → "Library"
3. Procure por "Google Sheets API"
4. Clique em "Google Sheets API"
5. Clique em "Enable"

### Etapa 5: Criar planilha no Google Sheets

1. Abra https://sheets.google.com
2. Crie uma nova planilha
3. Renomeie para "DOU - IFMS" (ou como preferir)
4. Copie o ID da URL:
   ```
   https://docs.google.com/spreadsheets/d/ESTE_AQUI_É_O_ID/edit
   ```

### Etapa 6: Configurar ID da planilha no projeto

1. Abra o arquivo: `config/config.py`
2. Encontre a linha:
   ```python
   SPREADSHEET_ID = None
   ```
3. Substitua por:
   ```python
   SPREADSHEET_ID = "seu_id_aqui"
   ```
   (Cole o ID copiado no passo anterior)

4. Salve o arquivo

## ✅ Testando tudo

### Teste 1: Verificar dependências

```bash
python -c "import requests, bs4, google.auth; print('✓ Todas as dependências instaladas')"
```

### Teste 2: Testar autenticação Google

```bash
python -c "from src.google_sheets import GoogleSheetsIntegration; gs = GoogleSheetsIntegration(); print('✓ Autenticado com sucesso!')"
```

Na primeira execução, será aberto um navegador para você fazer login no Google.

### Teste 3: Testar scraper

```bash
python -c "from src.dou_scraper import DOUScraper; s = DOUScraper(); print('✓ Scraper funcionando!')"
```

## 🚀 Primeira execução

Agora execute o scraper:

```bash
python main.py
```

Você deve ver:
- ✓ Scraping do DOU
- ✓ Filtragem de resultados
- ✓ Backup em JSON
- ✓ Exportação para Google Sheets
- ✓ Link da planilha

## 📋 Checklist pós-instalação

- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Credenciais baixadas (`credentials/credentials.json` existe)
- [ ] Google Sheets API ativada no Cloud Console
- [ ] Planilha criada no Google Sheets
- [ ] ID da planilha configurado em `config/config.py`
- [ ] Primeira execução bem-sucedida (`python main.py`)

## 🆘 Problemas Comuns

### "credentials.json não encontrado"
```
Solução: Copie o arquivo para credentials/credentials.json
mv ~/Downloads/client_secret_*.json ./credentials/credentials.json
```

### "Spreadsheet not found" ou erro 404
```
Solução: Verifique o SPREADSHEET_ID em config/config.py
```

### "Permission denied" na planilha
```
Solução: Certifique-se de que você compartilhou a planilha com sua conta
```

### Erro de autenticação na primeira execução
```
Solução: Isso é normal! Um navegador abrirá para login.
Se não abrir:
1. Procure pela URL na saída do terminal
2. Abra manualmente no navegador
3. Complete o login
```

## 📞 Contato & Suporte

Se tiver dúvidas ou problemas, abra uma issue no GitHub.

---

**Pronto! 🎉 Seu scraper está configurado e pronto para usar!**
