# ✅ Checklist de Instalação & Configuração

Siga este checklist passo-a-passo para configurar o DOU Scraper com sucesso.

## 📋 Pré-requisitos

- [ ] Python 3.8+ instalado
- [ ] Git instalado (opcional, para clonar)
- [ ] Conta do Google ativa
- [ ] Editor de texto (VS Code, Sublime, etc)
- [ ] Acesso à internet

## 🔧 Instalação Básica

### Passo 1: Obter o Código
```bash
# Opção A: Com Git
git clone https://github.com/leonardoolivera/testecodex.git
cd testecodex

# Opção B: Download manual
# Baixe o ZIP do GitHub e extraia
```
- [ ] Código obtido com sucesso
- [ ] Pasta `testecodex` existe no seu computador

### Passo 2: Instalar Dependências
```bash
# Opção A: Script automático (recomendado)
bash setup.sh

# Opção B: Manual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
- [ ] Environment virtual criado
- [ ] Dependências instaladas sem erros

## 🔑 Configuração Google Sheets

### Passo 3: Google Cloud Console
```
https://console.cloud.google.com/
```
- [ ] Nova conta de projeto criada
- [ ] Nome: `DOU-Scraper` (ou preferência)
- [ ] Projeto selecionado

### Passo 4: Ativar Sheets API
```
APIs & Services > Library > "Google Sheets API"
```
- [ ] Google Sheets API ativada

### Passo 5: Google OAuth 2.0
```
APIs & Services > Credentials > Create Credentials > OAuth 2.0 Client ID
```
- [ ] OAuth consent screen configurado
- [ ] Tipo: Desktop application
- [ ] JSON baixado
- [ ] Nomeado para: `credentials.json`
- [ ] Movido para: `credentials/credentials.json`

**Verificar:**
```bash
ls -la credentials/credentials.json
# Deve aparecer o arquivo
```
- [ ] Arquivo `credentials.json` em `credentials/`

### Passo 6: Google Sheets
```
https://sheets.google.com/
```
- [ ] Planilha criada
- [ ] Nome: `DOU - IFMS`
- [ ] ID copiado da URL
- [ ] ID guardado em segurança

## ⚙️ Configurar o Projeto

### Passo 7: Arquivo de Configuração
```bash
# Edite com seu editor favorito
nano config/config.py   # Linux/Mac
notepad config\config.py # Windows
```

Procure por:
```python
SPREADSHEET_ID = None
```

Substitua por:
```python
SPREADSHEET_ID = "seu_id_aqui"
```

- [ ] Arquivo `config.py` editado
- [ ] `SPREADSHEET_ID` configurado com ID correto

**Verificação:**
```bash
python -c "from config.config import SPREADSHEET_ID; print(SPREADSHEET_ID)"
# Deve aparecer: seu_id_aqui
```
- [ ] SPREADSHEET_ID válido

## 🧪 Testes

### Passo 8: Verificar Instalação
```bash
python -c "import requests, bs4, google.auth; print('✓ OK')"
```
- [ ] Todas as dependências carregadas

### Passo 9: Autenticação Google
```bash
python -c "from src.google_sheets import GoogleSheetsIntegration; print('✓')"
```

- [ ] Navegador abrirá (normal!)
- [ ] Faça login com sua conta Google
- [ ] Autorice o acesso
- [ ] Retornar ao terminal com ✓
- [ ] Token salvo em `credentials/token.pickle`

## 🚀 Primeira Execução

### Passo 10: Executar o Scraper
```bash
python main.py
```

Espere a execução completar. Você deve ver:

```
============================================================
Iniciando DOU Scraper - Instituto Federal de Mato Grosso do Sul
============================================================

[1/4] Iniciando scraping do DOU...
✓ XX resultados encontrados

[2/4] Filtrando resultados...
✓ X resultados após filtro

[3/4] Salvando backup em JSON...
✓ Backup salvo em: resultados_dou_YYYYMMDD_HHMMSS.json

[4/4] Exportando para Google Sheets...
✓ Dados exportados com sucesso!
✓ Acesse a planilha: https://docs.google.com/spreadsheets/d/...

============================================================
RESUMO DA EXECUÇÃO
============================================================
Resultados encontrados: XX
Resultados após filtro: X
Linhas adicionadas: X
Arquivo JSON: resultados_dou_YYYYMMDD_HHMMSS.json
Planilha: https://docs.google.com/spreadsheets/d/...
============================================================
```

- [ ] Execução completada sem erros
- [ ] X resultados encontrados
- [ ] Dados exportados para Sheets

### Passo 11: Verificar Planilha
```
Visite: https://docs.google.com/spreadsheets/d/SEU_ID/edit
```
- [ ] Planilha existe
- [ ] Headers adicionados (Data, Título, Seção, etc)
- [ ] Dados visualizados
- [ ] Informações de IFMS presentes

## 📚 Documentação

- [ ] Li [README.md](./README.md)
- [ ] Li [ARQUITETURA.md](./ARQUITETURA.md)
- [ ] Consultei [FAQ.md](./FAQ.md) se tive dúvidas
- [ ] Revisei [EXEMPLO_DADOS.md](./EXEMPLO_DADOS.md)

## 🎓 Experimentar

### Passo 12: Menu Interativo
```bash
python exemplos.py
```
- [ ] Menu interativo abriu
- [ ] Testei pelo menos 1 exemplo
- [ ] Entendi como funciona

## ⚙️ Operação

### Passo 13: Usar com Makefile (opcional)
```bash
make help     # Ver todos os comandos
make run      # Executar scraper
make examples # Exemplos interativos
```
- [ ] Makefile funciona em seu sistema (Linux/Mac)

### Passo 14: Docker (opcional)
```bash
docker-compose up
```
- [ ] Docker instalado (se quiser usar)
- [ ] Container executa com sucesso (opcional)

## 📅 Agendamento (opcional)

### Opção A: Crontab (Linux/Mac)
```bash
crontab -e
# Adicione:
0 6 * * * cd ~/testecodex && python main.py
```
- [ ] Crontab configurado

### Opção B: Task Scheduler (Windows)
- [ ] Tarefa criada no Windows Task Scheduler

### Opção C: GitHub Actions
- [ ] Secrets configurados no repositório
- [ ] Workflow ativa automaticamente

## 🔒 Segurança

- [ ] `credentials/credentials.json` em `.gitignore`
- [ ] `credentials/token.pickle` em `.gitignore`
- [ ] Credenciais NUNCA commitadas no Git
- [ ] Permissões da planilha verificadas

## 📊 Monitoramento

- [ ] Arquivo `scraper.log` gerado
- [ ] Logs são legíveis e úteis
- [ ] Erros registrados corretamente
- [ ] Relatório exibido ao final

## ✨ Customização (opcional)

- [ ] Li [config/config.py](./config/config.py)
- [ ] Entendi as configurações disponíveis
- [ ] Fiz personalizações conforme necessário
- [ ] Testei as mudanças

## 🐛 Troubleshooting

Se algo não funcionar:

- [ ] Verifiquei `scraper.log`
- [ ] Consultei [FAQ.md](./FAQ.md)
- [ ] Testei `python exemplos.py`
- [ ] Verifiquei internet: `ping google.com`
- [ ] Verifiquei credenciais: `ls -la credentials/`
- [ ] Re-autentiquei se necessário
- [ ] Deletei `credentials/token.pickle` e tentei novamente

## 📞 Suporte

Se ainda tiver problemas:

- [ ] Li toda a documentação
- [ ] Procurei no GitHub Issues
- [ ] Abri uma nova issue com detalhes
- [ ] Incluí logs e mensagens de erro

---

## 🎉 Conclusão

Se todos os checkboxes acima estão marcados, você está **pronto para usar**!

### Próximos Passos:

1. **Use regularmente**: `python main.py`
2. **Agende**: Configure execução automática
3. **Customize**: Adicione filtros/palavras-chave conforme necessário
4. **Explore**: Analise os dados na planilha
5. **Contribua**: Envie melhorias via GitHub!

---

**Data de conclusão**: ___/___/______

**Pronto! 🚀**

*Checklist criado em: 24/03/2026*
