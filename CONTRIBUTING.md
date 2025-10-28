# Guia de Contribuição

Obrigado por considerar contribuir para o Dashboard de Saúde Mental! Este documento fornece diretrizes para contribuir com o projeto.

## Como Contribuir

### Reportando Bugs

Se você encontrou um bug, por favor abra uma issue incluindo:

- Descrição clara do problema
- Passos para reproduzir o bug
- Comportamento esperado vs. comportamento atual
- Screenshots (se aplicável)
- Versão do Python e das dependências

### Sugerindo Melhorias

Para sugerir novas funcionalidades ou melhorias:

- Abra uma issue com o prefixo `[Feature]`
- Descreva claramente a funcionalidade desejada
- Explique por que essa melhoria seria útil
- Forneça exemplos de uso, se possível

### Pull Requests

1. **Fork o projeto** e crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```

2. **Siga os padrões de código**:
   - Use nomes descritivos para variáveis e funções
   - Adicione comentários quando necessário
   - Mantenha o código limpo e legível
   - Siga as convenções PEP 8 para Python

3. **Teste suas mudanças**:
   - Execute o dashboard localmente
   - Verifique se não há erros no console
   - Teste em diferentes navegadores (se aplicável)

4. **Commit suas mudanças**:
   ```bash
   git commit -m "feat: adiciona nova funcionalidade X"
   ```
   
   Use prefixos nos commits:
   - `feat:` para novas funcionalidades
   - `fix:` para correções de bugs
   - `docs:` para mudanças na documentação
   - `style:` para formatação de código
   - `refactor:` para refatoração de código
   - `test:` para adição de testes

5. **Push para sua branch**:
   ```bash
   git push origin feature/nome-da-feature
   ```

6. **Abra um Pull Request**:
   - Descreva claramente o que foi alterado
   - Referencie issues relacionadas
   - Aguarde revisão do código

## Padrões de Código

### Python

- Siga o [PEP 8](https://pep8.org/)
- Use 4 espaços para indentação
- Limite linhas a 100 caracteres quando possível
- Use docstrings para funções e classes

### Streamlit

- Use `@st.cache_data` para funções que carregam dados
- Organize o código em seções claras
- Adicione títulos e subtítulos descritivos
- Use componentes do Streamlit de forma consistente

### Visualizações

- Prefira Plotly para gráficos interativos
- Use cores consistentes com o tema do dashboard
- Adicione títulos e labels claros nos gráficos
- Certifique-se de que os gráficos são responsivos

## Estrutura de Arquivos

Ao adicionar novos arquivos, siga a estrutura existente:

```
mental-health-dashboard/
├── app.py                    # Página principal
├── pages/                    # Novas páginas do dashboard
│   └── N_NomeDaPagina.py    # Use numeração para ordem
├── data/                     # Novos datasets
├── utils/                    # Funções auxiliares (se necessário)
└── .streamlit/              # Configurações
```

## Adicionando Novas Páginas

Para adicionar uma nova página ao dashboard:

1. Crie um arquivo em `pages/` seguindo o padrão: `N_NomeDaPagina.py`
2. A numeração (N) define a ordem no menu
3. Inclua imports necessários:
   ```python
   import streamlit as st
   import pandas as pd
   import plotly.express as px
   ```

4. Adicione um título claro:
   ```python
   st.title("📊 Título da Página")
   ```

5. Mantenha o código organizado e comentado

## Adicionando Dependências

Se sua contribuição requer novas bibliotecas:

1. Adicione ao `requirements.txt` com versão mínima:
   ```
   nova-biblioteca>=1.0.0
   ```

2. Documente o uso da biblioteca no PR
3. Certifique-se de que é realmente necessária

## Código de Conduta

- Seja respeitoso e profissional
- Aceite críticas construtivas
- Foque no que é melhor para o projeto
- Ajude outros contribuidores

## Dúvidas?

Se tiver dúvidas sobre como contribuir:

- Abra uma issue com a tag `[Dúvida]`
- Entre em contato com os mantenedores
- Consulte a documentação do [Streamlit](https://docs.streamlit.io/)

---

Agradecemos sua contribuição! 🎉

