# 🧠 Dashboard de Saúde Mental no Trabalho

Dashboard interativo desenvolvido em Streamlit para análise e visualização de dados relacionados à saúde mental no ambiente de trabalho. Este projeto foi desenvolvido para a entrega da disciplina **Projetos 5** do curso de **Gestão de Tecnologia da Informação (GTI)** - CESAR School.

## 📋 Sobre o Projeto

Este dashboard permite explorar e analisar três datasets relacionados à saúde mental no trabalho, seguindo princípios de **Data Visualization** e **Data Storytelling** para apresentações orais. A interface prioriza clareza visual e minimalismo textual, com foco em visualizações interativas usando Plotly Express.

### 🎯 Objetivos

- Identificar grupos de risco de burnout e estresse
- Analisar associações entre carga de trabalho e saúde mental
- Comparar impacto de diferentes modalidades de trabalho (remoto, híbrido, presencial)
- Avaliar políticas organizacionais em termos de risco de burnout
- Segmentar análises por departamento, região e ocupação

### 📊 Datasets

O projeto integra três datasets principais:

- **Dataset Principal** (`dataset_principal.csv`): Dados gerais sobre saúde mental, hábitos e características individuais
- **Dataset Burnout** (`dataset_burnout.csv`): Análise específica de níveis de estresse e burnout por região
- **Dataset Workplace** (`dataset_workplace.csv`): Informações sobre modalidades de trabalho, satisfação e políticas organizacionais

## ✨ Funcionalidades

### 📊 Visualizações Interativas

- **Plotly Express**: Gráficos de alta qualidade usando `px.histogram`, `px.bar`, `px.pie`, `px.scatter`, `px.violin`, `px.box`, `px.imshow`
- **Visualizações minimalistas**: Foco em clareza visual com texto reduzido (títulos, labels e KPIs essenciais)
- **Paleta de cores semântica**: Vermelho para alto risco, verde para baixo risco, amarelo para risco médio
- **Gráficos responsivos**: Adaptação automática ao tamanho da tela

### 🎯 Filtros Dinâmicos

- **Filtro por cargo/ocupação**: Análise por diferentes profissões
- **Filtro por modalidade de trabalho**: Remoto, híbrido ou presencial
- **Filtro por carga horária semanal**: Range slider para horas trabalhadas
- **Filtro por segmentos**: Departamento, região ou política (em páginas específicas)

### 📈 Métricas e KPIs

- **KPIs contextuais**: Métricas específicas por página (respondentes, estresse médio, % burnout alto, horas semanais)
- **Comparações visuais**: Deltas e rankings para identificar padrões
- **Análise segmentada**: Identificação de grupos críticos (top 3 por risco)

### 📱 Interface

- **Layout responsivo**: Design wide para aproveitar melhor o espaço
- **Tema dark**: Configuração visual consistente
- **Navegação multipágina**: 6 páginas especializadas
- **Tooltips informativos**: Ajuda contextual nos filtros e métricas

## 🗂️ Estrutura das Páginas

O dashboard possui 6 páginas principais, cada uma focada em uma análise específica:

### 1. 🧠 Panorama da Saúde Mental (`1_Visao_Geral.py`)
**Página inicial** com visão geral dos dados:
- KPIs: Número de respondentes, estresse médio, % burnout alto, horas semanais médias
- Distribuição de estresse (histograma)
- Composição de níveis de burnout (gráfico de pizza)
- Heatmap de correlação entre variáveis-chave

### 2. 🔥 Burnout & Carga de Trabalho (`pages/2_Burnout.py`)
**Análise da associação** entre intensidade de trabalho e risco:
- KPIs: % burnout alto, estresse médio, horas semanais
- Scatter plot: Horas de trabalho × Estresse (com linha de tendência OLS)
- Violin plot: Estresse por faixa de horas (<35h, 35–45h, >45h)
- Ranking horizontal: Cargos com maior risco de burnout

### 3. 🏢 Ambiente & Políticas Organizacionais (`pages/3_Politica_Organizacional.py`)
**Comparação de políticas** em termos de risco:
- KPIs: Número de políticas distintas, % burnout alto geral, estresse médio
- Gráfico empilhado: Distribuição de burnout (baixo/médio/alto) por política
- Ranking horizontal: Políticas com maior % de burnout alto
- Tabela resumo: N, estresse médio, taxa de burnout por política

### 4. 🏠 Modalidades de Trabalho (`pages/4_Modalidade_Trabalho.py`)
**Comparação entre remoto, híbrido e presencial**:
- KPIs por modalidade: % burnout alto e estresse médio
- Violin plot: Distribuição de estresse por modalidade
- Bar chart: % burnout alto por modalidade
- **Análise avançada**: Deltas de risco entre modalidades por segmento (heatmap interativo)

### 5. 🧩 Perfis & Segmentos (`pages/5_Perfis_Segmentos.py`)
**Identificação de grupos** com maior estresse e burnout:
- Seleção de dimensão: Região, Ocupação ou Política
- KPIs: Número de segmentos, % em segmentos críticos (top 3), % burnout alto geral
- Ranking horizontal: Segmentos com maior % de burnout alto
- Bar chart: Estresse médio por segmento
- Tabela resumo: N, estresse médio, horas médias, % burnout alto

### 6. ℹ️ Sobre & Métodos (`pages/6_Sobre_Metodos.py`)
**Documentação** do projeto:
- Problema e perguntas de pesquisa
- Dados e preparação
- Metodologia (CRISP-DM adaptado)
- Limitações e cuidados
- Equipe e ferramentas

## 🔧 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.8 ou superior** (recomendado: 3.10+)
  - Verifique com: `python3 --version` ou `python --version`
- **pip** (gerenciador de pacotes Python)
  - Geralmente vem instalado com Python
  - Verifique com: `pip --version`
- **Git** (apenas se for clonar o repositório)
  - Verifique com: `git --version`

**Nota**: Se você já tem o projeto baixado e um ambiente virtual criado, pode pular direto para a seção "Execução".

## 🚀 Instalação e Execução Local

> **💡 Como usar os comandos**: 
> - **No GitHub**: Clique no ícone de "copiar" (📋) que aparece ao passar o mouse sobre cada bloco de código
> - **Em editores de texto**: Selecione o texto do comando e copie (Ctrl+C / Cmd+C)
> - **No terminal**: Cole o comando (Ctrl+V / Cmd+V) e pressione **Enter** para executar
> - Execute os comandos **um por vez**, na ordem apresentada

### Opção A: Primeira vez (instalação completa)

#### 1. Clone ou baixe o repositório

Se você ainda não tem o projeto:

```bash
git clone https://github.com/Bruno-fmaciel/mental-health-dashboard.git
```

```bash
cd mental-health-dashboard
```

**OU** se você já tem o projeto baixado, apenas navegue até a pasta:

```bash
cd /caminho/para/mental-health-dashboard
```

#### 2. Crie um ambiente virtual (se ainda não tiver)

**Importante**: Se a pasta `venv/` já existe no projeto, você pode pular esta etapa e ir direto para o passo 3.

**Windows:**
```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

**Como saber se o ambiente está ativado?**
- No Windows OU macOS/Linux: você verá `(venv)` no início do prompt

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Isso instalará todas as bibliotecas necessárias (Streamlit, Pandas, Plotly, etc.).

**Tempo estimado**: 1-3 minutos dependendo da sua conexão.

#### 4. Verifique se os datasets estão presentes

Certifique-se de que a pasta `data/` contém os três arquivos CSV:
- `dataset_principal.csv`
- `dataset_burnout.csv`
- `dataset_workplace.csv`

Se algum arquivo estiver faltando, o dashboard ainda funcionará, mas algumas análises podem não estar disponíveis.

### Opção B: Execução rápida (ambiente já configurado)

Se você já configurou o ambiente anteriormente, execute os comandos abaixo na ordem:

**1. Navegue até a pasta do projeto:**
```bash
cd /caminho/para/mental-health-dashboard
```

**2. Ative o ambiente virtual:**

*Windows:*
```bash
venv\Scripts\activate
```

*macOS/Linux:*
```bash
source venv/bin/activate
```

**3. Execute o dashboard:**
```bash
streamlit run 1_Visao_Geral.py
```

### 5. Acesse o dashboard

Após executar o comando `streamlit run 1_Visao_Geral.py`:

1. O Streamlit abrirá automaticamente no seu navegador
2. A URL será: `http://localhost:8501`
3. Se não abrir automaticamente, copie e cole a URL no navegador

**O que você verá:**
- Uma página inicial com KPIs e gráficos interativos
- Um menu lateral com filtros para explorar os dados
- Links para outras páginas do dashboard no menu lateral

### 6. Navegar pelo dashboard

O dashboard possui 6 páginas principais, acessíveis pelo menu lateral:

1. **🧠 Panorama da Saúde Mental** - Página inicial com indicadores globais
2. **🔥 Burnout & Carga de Trabalho** - Análise detalhada de níveis de estresse e burnout
3. **🏢 Ambiente & Políticas Organizacionais** - Impacto das políticas organizacionais
4. **🏠 Modalidades de Trabalho** - Comparação entre remoto, híbrido e presencial
5. **🧩 Perfis & Segmentos** - Identificação de grupos de risco
6. **ℹ️ Sobre & Métodos** - Documentação e metodologia do projeto

### 7. Parar o servidor

Para parar o dashboard:
- No terminal onde o Streamlit está rodando, pressione: `Ctrl + C` (Windows/Linux) ou `Cmd + C` (macOS)

**Importante**: Mantenha o terminal aberto enquanto o dashboard estiver rodando. Fechar o terminal encerrará o servidor.

## 🎯 Primeiros Passos

Após executar o dashboard pela primeira vez:

1. **Explore os filtros**: Use o menu lateral para filtrar por cargo, modalidade de trabalho, horas semanais, etc.
2. **Navegue pelas páginas**: Clique nos links no menu lateral para ver diferentes análises
3. **Interaja com os gráficos**: Os gráficos Plotly são interativos - você pode fazer zoom, passar o mouse para ver detalhes, etc.
4. **Compare segmentos**: Use a página "Perfis & Segmentos" para identificar grupos de risco
5. **Análise avançada**: Explore a seção de deltas na página "Modalidades de Trabalho" para análises comparativas detalhadas

**Dica**: Comece pela página "Panorama da Saúde Mental" para ter uma visão completa dos dados antes de explorar análises específicas.

## 📁 Estrutura do Projeto

```
mental-health-dashboard/
├── 1_Visao_Geral.py                    # 🏠 Arquivo principal - execute este para iniciar
├── pages/                              # 📄 Páginas adicionais do dashboard
│   ├── 2_Burnout.py                    # Análise de burnout e carga de trabalho
│   ├── 3_Politica_Organizacional.py   # Políticas organizacionais
│   ├── 4_Modalidade_Trabalho.py       # Modalidades de trabalho (remoto/híbrido/presencial)
│   ├── 5_Perfis_Segmentos.py          # Análise de segmentos e perfis
│   └── 6_Sobre_Metodos.py              # Documentação e metodologia
├── data/                               # 📊 Datasets CSV (obrigatórios)
│   ├── dataset_principal.csv
│   ├── dataset_burnout.csv
│   └── dataset_workplace.csv
├── utils/                              # 🛠️ Utilitários e funções auxiliares
│   ├── __init__.py                    # Exportações centralizadas
│   ├── data_io.py                     # Carregamento e normalização de dados
│   ├── charts.py                      # Funções de visualização (Plotly Express)
│   └── theming.py                     # Configurações de tema
├── insights/                           # 💡 Módulos de análise e insights
│   ├── __init__.py
│   ├── burnout.py
│   ├── enviroments.py
│   ├── modalidades.py
│   ├── overview.py
│   └── segments.py
├── ui/                                 # 🎨 Componentes de interface
│   └── insight_box.py                 # Componente de exibição de insights
├── .streamlit/                         # ⚙️ Configurações do Streamlit
│   └── config.toml                    # Tema e configurações visuais
├── venv/                               # 🐍 Ambiente virtual Python (gerado localmente)
├── requirements.txt                    # 📦 Lista de dependências
├── .gitignore                          # Arquivos ignorados pelo Git
├── LICENSE                             # Licença MIT
├── CONTRIBUTING.md                     # Guia de contribuição
└── README.md                           # Este arquivo
```

**Arquivos importantes:**
- `1_Visao_Geral.py`: Execute este arquivo para iniciar o dashboard
- `data/*.csv`: Os datasets são carregados automaticamente pelo dashboard
- `requirements.txt`: Contém todas as dependências necessárias
- `utils/charts.py`: Centraliza todas as funções de visualização usando Plotly Express

## 🎨 Princípios de Design

Este dashboard foi desenvolvido seguindo princípios de **Data Visualization** e **Data Storytelling**:

### Visualização
- **Plotly Express**: Uso prioritário de funções de alto nível (`px.*`) para gráficos consistentes
- **Minimalismo textual**: Apenas títulos, subtítulos curtos, labels de eixos e KPIs essenciais
- **Cores semânticas**: Vermelho para alto risco, verde para baixo risco, amarelo para risco médio
- **Layout limpo**: Uso de containers e colunas para organização visual

### Storytelling
- **Narrativa visual**: Os gráficos contam a história; o texto é mínimo
- **Progressão lógica**: Da visão geral para análises específicas
- **Comparações diretas**: Rankings e deltas para destacar diferenças
- **Foco em insights**: Identificação clara de grupos de risco e padrões

### Arquitetura
- **Modularidade**: Funções de gráficos centralizadas em `utils/charts.py`
- **Reutilização**: Componentes compartilhados (filtros, KPIs, temas)
- **Manutenibilidade**: Código organizado e documentado

## 📊 Datasets

Os datasets utilizados contêm informações sobre:

- **Demographics**: Gênero, idade, localização geográfica
- **Work Environment**: Tipo de trabalho, ambiente, carga horária semanal
- **Mental Health**: Níveis de estresse (0-10), burnout (baixo/médio/alto), satisfação
- **Remote Work**: Dados sobre trabalho remoto, híbrido e presencial
- **Organizational Policies**: Políticas de suporte à saúde mental

### Normalização de Dados

O projeto normaliza automaticamente os três datasets para um formato unificado:
- `work_mode`: Padronizado para "remote", "hybrid", "onsite"
- `stress_score`: Escala 0-10
- `burnout_level`: Categorias "low", "medium", "high"
- `hours_per_week`: Horas trabalhadas por semana
- `segment`: Departamento (workplace) ou Região (burnout)

## 🔧 Troubleshooting (Solução de Problemas)

### Problema: "ModuleNotFoundError" ou "No module named 'streamlit'"

**Solução**: 
1. Certifique-se de que o ambiente virtual está ativado (você deve ver `(venv)` no prompt)
2. Execute:
```bash
pip install -r requirements.txt
```

### Problema: "FileNotFoundError" ao carregar datasets

**Solução**: 
1. Verifique se a pasta `data/` existe e contém os arquivos CSV
2. Certifique-se de estar executando o comando na pasta raiz do projeto
3. Verifique os caminhos dos arquivos em `utils/data_io.py`

### Problema: O dashboard não abre no navegador

**Solução**: 
1. Copie a URL mostrada no terminal (geralmente `http://localhost:8501`)
2. Cole no navegador manualmente
3. Verifique se outra aplicação não está usando a porta 8501

### Problema: "Port already in use"

**Solução**: 
1. Pare outros processos Streamlit que possam estar rodando
2. Ou use uma porta diferente:
```bash
streamlit run 1_Visao_Geral.py --server.port 8502
```

### Problema: Gráficos não aparecem ou dados estão vazios

**Solução**: 
1. Verifique se os arquivos CSV na pasta `data/` não estão corrompidos
2. Verifique o console do navegador (F12) para erros JavaScript
3. Tente limpar o cache do Streamlit:
```bash
streamlit cache clear
```

### Problema: Filtros não funcionam ou retornam dados vazios

**Solução**:
1. Verifique se os datasets contêm dados nas colunas filtradas
2. Ajuste os filtros na sidebar para valores mais amplos
3. Verifique se há dados suficientes após aplicar múltiplos filtros simultaneamente

## 🌐 Deploy no Streamlit Cloud

### Passo 1: Prepare o repositório

Certifique-se de que todos os arquivos necessários estão commitados:
- `1_Visao_Geral.py` (arquivo principal)
- `requirements.txt`
- Pasta `data/` com os datasets (ou configure para carregar de outra fonte)
- Pasta `pages/` com as páginas adicionais
- Pasta `utils/` com os módulos utilitários
- Pasta `insights/` com os módulos de análise
- Pasta `ui/` com os componentes de interface
- Pasta `.streamlit/` com configurações (opcional)

### Passo 2: Acesse o Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"

### Passo 3: Configure o deploy

1. Selecione o repositório: `Bruno-fmaciel/mental-health-dashboard`
2. Branch: `main`, `master` ou `developer` (conforme sua estrutura)
3. **Main file path**: `1_Visao_Geral.py` ⚠️ (não `app.py`)
4. Clique em "Deploy!"

**Nota**: O Streamlit Cloud detecta automaticamente as páginas na pasta `pages/` e cria a navegação lateral.

### Passo 4: Configurações avançadas (opcional)

Se precisar adicionar secrets (APIs, credenciais):
1. No Streamlit Cloud, vá em "Settings" > "Secrets"
2. Adicione suas variáveis no formato TOML
3. Use `st.secrets["chave"]` no código para acessá-las

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** (≥1.28.0) - Framework para criação de dashboards interativos
- **[Pandas](https://pandas.pydata.org/)** (≥2.0.0) - Manipulação e análise de dados
- **[Plotly](https://plotly.com/)** (≥5.17.0) - Visualizações interativas (Plotly Express)
- **[NumPy](https://numpy.org/)** (≥1.24.0) - Computação numérica
- **[Matplotlib](https://matplotlib.org/)** (≥3.7.0) - Visualizações estáticas (suporte)
- **[Seaborn](https://seaborn.pydata.org/)** (≥0.12.0) - Visualizações estatísticas (suporte)
- **[Statsmodels](https://www.statsmodels.org/)** (≥0.14.0) - Modelagem estatística (tendências OLS)

## 📚 Referências e Metodologia

### Metodologia CRISP-DM (Adaptado)
1. Entendimento do negócio
2. Entendimento dos dados
3. Preparação da base integrada
4. Modelagem visual (dashboards e KPIs)
5. Avaliação de hipóteses
6. Deploy (Streamlit Cloud)

### Princípios Aplicados
- **Storytelling com Dados** (Cole Nussbaumer Knaflic)
- **Information Dashboard Design** (Stephen Few)
- **Boas práticas de visualização de dados** (Plotly Express)

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes sobre o processo de contribuição.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Equipe

- **Bruno Maciel** - [@Bruno-fmaciel](https://github.com/Bruno-fmaciel)
- **Camila Oliveira** - [@camilamariaoliveira](https://github.com/camilamariaoliveira)
- **Maria Clara Medeiros**
- **Yuri Tavares**
- **Rodrigo Lyra**
- **Artur Tavares**

## 📧 Contato

Para dúvidas ou sugestões:
- Abra uma [issue](https://github.com/Bruno-fmaciel/mental-health-dashboard/issues) no GitHub
- Entre em contato com os autores através do GitHub

## 🙏 Agradecimentos

- **CESAR School** - GTI - Projetos 5
- **Projeto SR2** - Material de Aula
- Comunidade Streamlit e Plotly

---

**Desenvolvido com ❤️ para análise de saúde mental no trabalho**
