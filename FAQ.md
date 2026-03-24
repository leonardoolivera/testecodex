# ❓ Perguntas Frequentes (FAQ)

## Instalação

### P: Python não está instalado. Como faço?
**R:** Baixe em [python.org](https://www.python.org/downloads/). Certifique-se de marcar "Add Python to PATH" durante a instalação.

### P: Que versão de Python preciso?
**R:** Python 3.8 ou superior. Recomendado: 3.11+

### P: Posso usar em Windows?
**R:** Sim! O scraper funciona em Windows, Mac e Linux. Alguns comandos no README podem variar.

### P: Tenho error "module not found"
**R:** Execute `pip install -r requirements.txt` de novo. Se persistir, delete a pasta `venv/` e recrie.

---

## Google Sheets

### P: Onde obtenho credentials.json?
**R:** Siga o [SETUP_GUIA.md](./SETUP_GUIA.md) - seção "Configuração Google Sheets".

### P: Qual é meu SPREADSHEET_ID?
**R:** Na URL: `https://docs.google.com/spreadsheets/d/ESTE_AQUI/edit`

### P: Posso usar uma planilha existente?
**R:** Sim! Coloque apenas o ID e execute `main.py`. Os headers serão adicionados automaticamente.

### P: Erro "The caller does not have permission"
**R:** Certifique-se de ter compartilhado a planilha com sua conta Google (a mesma usada no login).

### P: Posso compartilhar a planilha com outras pessoas?
**R:** Sim! Compartilhe atualmente como faria com qualquer Google Sheets.

### P: E se eu tiver múltiplas planilhas?
**R:** Configure `SPREADSHEET_ID` em `config/config.py` para cada uma. Você pode executar múltiplas instâncias.

---

## Scraping

### P: Aparecer muitas publicações de outras instituições?
**R:** Sim, às vezes. Os filtros buscam por "IFMS" no título/resumo/órgão. Purifique manualmente na planilha se necessário.

### P: Como adiciono mais palavras-chave?
**R:** Edite `config/config.py` - seção `SEARCH_KEYWORDS`:
```python
SEARCH_KEYWORDS = [
    "Instituto Federal de Mato Grosso do Sul",
    "IFMS",
    "Federal Mato Grosso",  # Adicione aqui
]
```

### P: Como busco por data específica?
**R:** Por enquanto, a API do DOU retorna via filtros padrão. Você pode filtrar manualmente na planilha.

### P: Quantos resultados por busca?
**R:** ~50-100 por keyword. Configure em `config/config.py`:
```python
SEARCH_LIMIT = 100
```

### P: O scraper para se houver erro?
**R:** Não! Ele registra o erro e continua. Verifi que o `scraper.log`.

---

## Execução

### P: Quanto tempo leva para executar?
**R:** Geralmente 1-2 minutos. Depende da conexão e do DOU.

### P: Posso rodar em background?
**R:** Sim! Use:
- **Linux/Mac**: `nohup python main.py &`
- **Windows**: Abra Task Scheduler e crie uma tarefa
- **Docker**: `docker-compose up -d`

### P: Como agendar para rodar automaticamente?
**R:** 3 opções:
1. **Crontab** (Linux/Mac): `0 6 * * * python main.py`
2. **Task Scheduler** (Windows)
3. **GitHub Actions**: Use `.github/workflows/scraper.yml`

### P: Posso pausar a execução?
**R:** Sim, pressione `Ctrl+C` no terminal.

### P: O que significa cada log?
**R:** Verifique `scraper.log`:
- INFO: Operações normais
- WARNING: Avisos (nenhum resultado, etc)
- ERROR: Erros que foram tratados
- DEBUG: Informações detalhadas

---

## Dados

### P: Onde ficam os dados?
**R:** 
- **Google Sheets**: Na planilha
- **Backup**: Em `resultados_dou_YYYYMMDD_HHMMSS.json`
- **Logs**: Em `scraper.log`

### P: Como exporto os dados?
**R:** 
- Google Sheets: Download direto (CSV, XLSX)
- JSON: Já está em `resultados_dou_*.json`
- SQL: Importe o JSON em um database

### P: Posso adicionar colunas personalizadas?
**R:** Sim! Edite `config/config.py` - `SHEET_COLUMNS` e depois `SHEET_COLUMNS` em `src/dou_scraper.py`

### P: Quanto tempo os dados ficam?
**R:** Indefinitivamente! Google Sheets tem limite de 10 milhões de células.

---

## Desenvolvimento

### P: Como faço testes?
**R:** Execute:
```bash
pytest tests/
# ou
make test
```

### P: Posso me adaptar o código?
**R:** Sim! É open source. Contribuições são bem-vindas!

### P: Tenho bug para relatar?
**R:** Abra uma issue no GitHub com:
- Descrição do problema
- Steps para reproduzir
- Mensagem de erro completa

### P: Como eu contribuo?
**R:** Leia [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## Segurança

### P: Minha senha Google pode ser roubada?
**R:** Não! OAuth 2.0 é seguro e você faz login diretamente no Google.

### P: Onde ficam minhas credenciais?
**R:** Localmente em `credentials/credentials.json` e `credentials/token.pickle`. Nunca são versionadas.

### P: E se eu perder credenciais?
**R:** Delete `credentials/token.pickle` e faça login de new.

### P: Posso usar em múltiplos servidores?
**R:** Não compartilhe `credentials/token.pickle` entre servidores. Faça login em cada um.

---

## Docker

### P: O que é Docker?
**R:** Containerização - run o código em um ambiente isolado e reproduzível.

### P: Preciso de Docker?
**R:** Não, é opcional. Útil para produção/servidores.

### P: Como uso?
**R:** Execute:
```bash
docker-compose up
```

### P: Como faço build da imagem?
**R:** 
```bash
docker build -t dou-scraper .
docker run dou-scraper
```

---

## GitHub Actions

### P: Como configuro CI/CD?
**R:** Use `.github/workflows/scraper.yml`. Siga as instruções no arquivo.

### P: Preciso de credit card?
**R:** Não! GitHub Actions é grátis para repositórios públicos.

### P: Como agendar?
**R:** A workflow já está agendada para 6 AM UTC. Edite se necessário.

---

## Troubleshooting Geral

### P: Nada funciona! Quer me ajuda?
**R:** 
1. Leia o [README.md](./README.md)
2. Leia o [SETUP_GUIA.md](./SETUP_GUIA.md)
3. Verifique `scraper.log`
4. Tente `python exemplos.py`
5. Abra uma issue no GitHub

### P: Como faço clean install?
**R:**
```bash
rm -rf venv credentials token.pickle *.json *.log
bash setup.sh
```

### P: Algo mudou e parou de funcionar?
**R:** Todas as mudanças estão em [CHANGELOG.md](./CHANGELOG.md)

### P: Tenho sugestão de melhoria
**R:** Abra uma discussion ou issue no GitHub!

---

## Performance

### P: The scraper é lente?
**R:** Normal 1-2 minutos. Se muito lento:
- Verifique internet: `ping google.com`
- Reduza `SEARCH_LIMIT` em `config/config.py`
- DOU pode estar lento

### P: Memory leak?
**R:** Não deve acontecer. Se tiver:
```bash
# Monitore
python -m memory_profiler main.py

# Ou reporte issue
```

### P: Como otimizo?
**R:** Possíveis otimizações:
1. Cache de resultados
2. Requisições em paralelo
3. Banco de dados local
4. API GraphQL do DOU (se existir)

---

## Migração

### P: Como processo meus dados antigos?
**R:** 
1. Exporte dados antigos para CSV
2. Importe manualmente na planilha
3. Use `exemplos.py` para adicionar dados customizados

### P: Posso trocar de planilha?
**R:** Sim! Configure `SPREADSHEET_ID` em `config/config.py` e execute `main.py` de novo.

---

## Contato

### P: Onde reporto bugs?
**R:** [GitHub Issues](https://github.com/leonardoolivera/testecodex/issues)

### P: Onde sugiro features?
**R:** [GitHub Discussions](https://github.com/leonardoolivera/testecodex/discussions)

### P: Preciso de suporte comercial?
**R:** Entre em contato: [adicionar email/contato]

---

**Não encontrou a resposta?** Abra uma issue! 🚀

*Última atualização: 24/03/2026*
