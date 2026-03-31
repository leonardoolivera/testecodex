# DOU Scraper - Instituto Federal de Mato Grosso do Sul

Um web scraper completo que escaneia o **Diário Oficial da União (DOU)**, filtra publicações relacionadas ao **Instituto Federal de Mato Grosso do Sul (IFMS)** e exporta os dados para uma **planilha do Google Sheets**.

## 📋 Funcionalidades

✅ **Scraping automático** do Diário Oficial da União  
✅ **Filtros inteligentes** por palavras-chave (IFMS)  
✅ **Exportação automática** para Google Sheets  
✅ **Backup em JSON** dos resultados  
✅ **Logging detalhado** de todas as operações  
✅ **Tratamento de erros** robusto  

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/leonardoolivera/testecodex.git
cd testecodex
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Google Sheets (IMPORTANTE)

#### Passo 1: Criar um projeto no Google Cloud

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative a **Sheets API**:
   - Vá para "APIs e Serviços"
   - Clique em "Ativar APIs e Serviços"
   - Procure por "Sheets API"
   - Clique em "Ativar"

#### Passo 2: Criar credenciais OAuth 2.0

1. Acesse "Credenciais" no Google Cloud Console
2. Clique em "Criar credenciais" → "ID do cliente OAuth 2.0"
3. Selecione "Aplicação de desktop"
4. Faça download do arquivo JSON
5. Renomeie para `credentials.json` e coloque na pasta `credentials/`

```bash
mv ~/Downloads/client_secret_*.json ./credentials/credentials.json
```

#### Passo 3: Criar uma planilha no Google Sheets

1. Acesse [Google Sheets](https://sheets.google.com)
2. Crie uma nova planilha com o nome "DOU - IFMS"
3. Copie o ID da URL:
   - URL: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`
   - O `{SPREADSHEET_ID}` é o código longo na URL

#### Passo 4: Configurar o ID da planilha

Edite o arquivo `config/config.py` e substitua:

```python
SPREADSHEET_ID = "seu_id_aqui"
```

pelo ID obtido no passo anterior.

## 🚀 Como usar

### Executar o scraper

```bash
python main.py
```

O script irá:
1. ✓ Fazer scraping do DOU
2. ✓ Filtrar por IFMS
3. ✓ Salvar backup em JSON
4. ✓ Exportar para Google Sheets
5. ✓ Exibir link da planilha

### Primeira execução

Na primeira execução, você será solicitado a fazer login no Google. Siga as instruções na tela para autorizar o acesso.

### Acessar os resultados

Depois da execução bem-sucedida, acesse a planilha em:
```
https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
```

## 📁 Estrutura do projeto

```
testecodex/
├── main.py                 # Script principal
├── requirements.txt        # Dependências Python
├── config/
│   └── config.py          # Configurações
├── src/
│   ├── dou_scraper.py     # Classe do scraper do DOU
│   └── google_sheets.py   # Integração com Google Sheets
├── credentials/           # Sua pasta de credenciais (NÃO VERSIONAR!)
│   ├── credentials.json   # Credenciais OAuth (seu arquivo)
│   └── token.pickle       # Token (gerado automaticamente)
└── README.md              # Este arquivo
```

## 🔧 Configurações

Edite `config/config.py` para personalizar:

| Configuração | Padrão | Descrição |
|---|---|---|
| `SEARCH_KEYWORDS` | `["Instituto Federal de Mato Grosso do Sul", "IFMS", ...]` | Palavras-chave de busca |
| `SEARCH_LIMIT` | `100` | Número máximo de resultados |
| `SHEET_NAME` | `"DOU - IFMS"` | Nome da aba na planilha |
| `TIMEOUT` | `10` | Timeout em segundos |

## 📊 Dados coletados

A planilha contém as seguintes colunas:

| Campo | Descrição |
|---|---|
| Data de Publicação | Data da publicação no DOU |
| Título | Título da publicação |
| Seção | Seção do DOU |
| Página | Número da página |
| URL | Link para o artigo completo |
| Resumo | Resumo/Ementa da publicação |
| Data de Coleta | Data e hora em que foi coletado |

## 🔍 Exemplos de uso

### Executar uma única vez
```bash
python main.py
```

### Agendar execução periódica (Linux/Mac)
Adicione ao crontab para rodar diariamente:
```bash
crontab -e
# Adicione a linha:
0 6 * * * cd ~/testecodex && python main.py >> cron.log 2>&1
```

### Executar com logging expandido
```bash
python main.py  # Logs aparecem no console e em scraper.log
```

## 📝 Logs

Os logs de execução são salvos em `scraper.log` para análise posterior.

## ⚙️ Solução de problemas

### "Arquivo de credenciais não encontrado"
- Certifique-se de ter baixado `credentials.json` do Google Cloud
- Coloque o arquivo na pasta `credentials/`

### "Planilha ID não encontrada"
- Verifique se o SPREADSHEET_ID está correto em `config/config.py`
- Certifique-se de ter acesso à planilha no Google Sheets

### "Erro de autenticação"
- Delete o arquivo `credentials/token.pickle`
- Execute novamente para reautenticar

### Nenhum resultado encontrado
- Verifique se a API do DOU está funcionando
- Tente alterar as palavras-chave em `config/config.py`
- Verifique a conexão de internet

## 🔐 Segurança

⚠️ **Importante:**
- Nunca faça commit de `credentials.json` ou `token.pickle`
- Adicione `credentials/` ao `.gitignore` (já está)
- Mantenha suas credenciais seguras

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Autor

Leonardo Oliveira

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para abrir issues e pull requests.

## 📞 Suporte

Para reportar problemas ou sugerir melhorias, abra uma issue no GitHub.

---

**Última atualização:** 24/03/2026
