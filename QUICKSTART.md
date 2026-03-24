# 🚀 Quickstart - DOU Scraper

**Comece em 5 minutos!**

## Instalação Rápida

```bash
# 1. Instale dependências
pip install -r requirements.txt

# 2. Abra config/config.py e coloque seu SPREADSHEET_ID

# 3. Coloque credentials.json em credentials/

# 4. Execute!
python main.py
```

## Configuração Detalhada

Se é a primeira vez, siga em ordem:

1. **Abra**: [SETUP_GUIA.md](./SETUP_GUIA.md) - Guia passo-a-passo completo
2. **Leia**: [README.md](./README.md) - Documentação completa
3. **Teste**: `python exemplos.py` - Menu interativo com exemplos

## O que o scraper faz?

```
Diário Oficial da União
         ↓
    [Scraper] → Busca por "IFMS"
         ↓
    [Filtro] → Valida menções a IFMS
         ↓
    [Backup] → Salva resultados em JSON
         ↓
  [Google Sheets] → Exporta para planilha
         ↓
    Você acessa!
```

## Estrutura

```
testecodex/
├── main.py             ← EXECUTE ISTO
├── exemplos.py         ← Menu interativo
├── config/config.py    ← Configure AQUI
├── src/                ← Código principal
│   ├── dou_scraper.py
│   └── google_sheets.py
└── credentials/        ← Coloque credentials.json AQUI
```

## Primeiros Passos

### 1️⃣ Cloar/baixar o projeto
```bash
git clone https://github.com/leonardoolivera/testecodex.git
cd testecodex
```

### 2️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar Google
- Visite [Google Cloud Console](https://console.cloud.google.com/)
- Crie um projeto novo
- Ative "Google Sheets API"
- Baixe credenciais OAuth 2.0 (Desktop application)
- Renomeie para `credentials.json` e coloque em `credentials/`

### 4️⃣ Criar planilha
- Visite [Google Sheets](https://sheets.google.com)
- Crie nova planilha chamada "DOU - IFMS"
- Copie o ID da URL: `https://docs.google.com/spreadsheets/d/COPY_AQUI/edit`

### 5️⃣ Configurar
Edite `config/config.py`:
```python
SPREADSHEET_ID = "cole_o_id_aqui"
```

### 6️⃣ Executar!
```bash
python main.py
```

Pronto! ✅ Uma janela do navegador abrirá para você fazer login no Google. Após login, o scraper executará automaticamente!

## Opções

### Testar componentes
```bash
# Teste scraper
python -c "from src.dou_scraper import DOUScraper; print('✓')"

# Teste Google Sheets
python -c "from src.google_sheets import GoogleSheetsIntegration; print('✓')"
```

### Exemplos interativos
```bash
python exemplos.py
```

Menu com 5 exemplos diferentes de uso.

### Rodar com Makefile
```bash
make run       # Executa o scraper
make install   # Instala dependências
make clean     # Limpa temporários
make examples  # Exemplos interativos
```

### Rodar em Docker
```bash
docker-compose up
```

## Troubleshooting

| Erro | Solução |
|------|---------|
| `credentials.json not found` | Coloque o arquivo em `credentials/` |
| `SPREADSHEET_ID not configured` | Configure em `config/config.py` |
| `Permission denied` | Certifique-se de ter acesso à planilha |
| `API not enabled` | Ative Google Sheets API no Cloud Console |

## Próximos Passos

- ✅ Customize as palavras-chave em `config/config.py`
- ✅ Agende execução com `crontab` ou `Task Scheduler`
- ✅ Adicione filtros mais específicos em `src/dou_scraper.py`
- ✅ Crie dashboards com os dados na planilha

## Documentação Completa

- 📖 [README.md](./README.md) - Documentação completa
- 📋 [SETUP_GUIA.md](./SETUP_GUIA.md) - Guia de configuração
- 💡 [EXEMPLO_DADOS.md](./EXEMPLO_DADOS.md) - Exemplos de dados

## Suporte

Problemas? Abra uma [issue no GitHub](https://github.com/leonardoolivera/testecodex/issues)

---

**Boa sorte! 🎉**
