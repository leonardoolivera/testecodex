# 🤝 Como Contribuir

Obrigado por se interessar em contribuir para o DOU Scraper!

## Tipos de Contribuição

### 🐛 Reportar Bugs

Se encontrou um bug, abra uma issue no GitHub:

```
Título: [BUG] Descrição concisa
Descrição:
- Como reproduzir
- Comportamento esperado
- Comportamento atual
- Sistema operacional
- Versão do Python
```

### 💡 Sugerir Melhorias

Tem uma ideia? Compartilhe:

```
Título: [FEATURE] Descrição da ideia
Descrição:
- Por que seria útil
- Exemplos de uso
- Possíveis implementações
```

### 📖 Melhorar Documentação

A documentação pode sempre ser melhorada! Sinta-se livre para:
- Corrigir erros de digitação
- Adicionar exemplos
- Esclarecer instruções
- Traduzir para outros idiomas

### 💻 Enviar Código

#### Pré-requisitos
- Python 3.8+
- Git
- Conhecimento básico de Python e web scraping

#### Passos

1. **Fork** o repositório
```bash
git clone https://github.com/SEU_USUARIO/testecodex.git
cd testecodex
```

2. **Crie uma branch** para sua feature
```bash
git checkout -b feature/sua-feature
```

3. **Instale dependências de desenvolvimento**
```bash
pip install -r requirements-dev.txt
```

4. **Faça suas mudanças**
```bash
# Edite os arquivos
# Teste suas mudanças
python exemplos.py
```

5. **Execute testes e linting**
```bash
make test
make lint
make format
```

6. **Commit com mensagem clara**
```bash
git add .
git commit -m "Descrição clara das mudanças"
```

7. **Push para seu fork**
```bash
git push origin feature/sua-feature
```

8. **Abra um Pull Request (PR)**
   - Descreva suas mudanças
   - Referencie issues relacionadas
   - Explique a motivação

## Padrões de Código

### Python
- Use [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Máximo 100 caracteres por linha
- Docstrings para funções/classes
- Type hints quando possível

### Exemplo
```python
def buscar_publicacoes(palavra_chave: str, limite: int = 10) -> list:
    """
    Busca publicações no DOU por palavra-chave.
    
    Args:
        palavra_chave: Termo para buscar
        limite: Número máximo de resultados
        
    Returns:
        Lista de publicações encontradas
    """
    # Implementação
    pass
```

### Commits
```
Padrão: [TIPO] Descrição breve

Exemplos:
[FIX] Corrige erro de timeout no scraper
[FEAT] Adiciona suporte a filtros de data
[DOCS] Melhora documentação de configuração
[TEST] Adiciona testes para dou_scraper.py
[REFACTOR] Reorganiza lógica de parsing
```

## Processo de Review

1. **Verificações Automáticas**
   - Testes passam (pytest)
   - Linting passa (pylint)
   - Formatação correcta (black)

2. **Review Humano**
   - Funcionalidade e implementação
   - Qualidade do código
   - Documentação
   - Testes adequados

3. **Aprovação e Merge**
   - Pelo menos 1 aprovação
   - Todos os testes passando
   - Sem conflitos com main

## Código de Conduta

- ✅ Seja respeitoso
- ✅ Seja inclusivo
- ✅ Seja profissional
- ✅ Seja colaborativo

## Perguntas?

- 📖 Leia a documentação: [README.md](./README.md)
- 💬 Abra uma discussion no GitHub
- 🐛 Reporte no issues
- 📧 Entre em contato

---

**Muito obrigado por contribuir! 🚀**
