# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O format é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-24

### ✨ Adicionado
- Scraper completo para Diário Oficial da União (DOU)
- Busca por palavras-chave (IFMS, Instituto Federal de Mato Grosso do Sul)
- Integração com Google Sheets API
- Autenticação OAuth 2.0
- Exportação automática de dados
- Backup em formato JSON
- Logging detalhado de operações
- Filtros inteligentes de conteúdo
- Tratamento robusto de erros

### 📦 Dependências Iniciais
- `requests` - HTTP requests
- `beautifulsoup4` - Web scraping
- `google-auth` - Autenticação Google
- `google-auth-oauthlib` - OAuth para Google
- `google-api-python-client` - Google Sheets API

### 📚 Documentação
- README.md - Documentação completa
- SETUP_GUIA.md - Guia de com configuração passo-a-passo
- QUICKSTART.md - Início rápido
- EXEMPLO_DADOS.md - Exemplos de dados
- CONTRIBUTING.md - Como contribuir

### 🛠️ Tools & DevOps
- Makefile para atalhos de tarefas
- Docker e docker-compose para containerização
- GitHub Actions para CI/CD
- Script de instalação automática (setup.sh)
- Testes unitários com pytest

### 🔧 Infraestrutura
- .gitignore para arquivos sensíveis
- .editorconfig para padronização
- requirements.txt e requirements-dev.txt
- EditorConfig para múltiplos editores

---

## Versões Futuras (Roadmap)

### v1.1.0 (Planejado)
- [ ] Filtros por data de publicação
- [ ] Interface web (Flask/FastAPI)
- [ ] Notificações por email
- [ ] Suporte a múltiplas instituições
- [ ] Dashboard de estatísticas

### v1.2.0 (Planejado)
- [ ] Banco de dados (SQLite/PostgreSQL)
- [ ] API REST
- [ ] Autenticação por usuário
- [ ] Histórico de buscas
- [ ] Exportação em múltiplos formatos

### v2.0.0 (Futuro)
- [ ] Aplicação web completa
- [ ] Machine learning para relevância
- [ ] Análise de sentimento
- [ ] Integração com Slack/Teams
- [ ] Mobile app

---

## Como Relatar Mudanças

Siga este formato para documentar mudanças:

- **Adicionado** para novas funcionalidades
- **Alterado** para mudanças em funcionalidades existentes
- **Descontinuado** para funcionalidades que serão removidas em breve
- **Removido** para funcionalidades removidas
- **Corrigido** para correções de bugs
- **Segurança** para vulnerabilidades

---

## Versionamento

Este projeto segue [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0) - Mudanças incompatíveis na API
- **MINOR** (0.X.0) - Novas funcionalidades compatíveis
- **PATCH** (0.0.X) - Correções de bugs

---

*Criado em: 24/03/2026*
