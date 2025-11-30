# 🧠 Dashboard de Saúde Mental no Trabalho

Dashboard interativo desenvolvido em Streamlit para análise e visualização de dados relacionados à saúde mental no ambiente de trabalho. Este projeto foi desenvolvido para a entrega da disciplina Projetos 5 do curso de Gestão de Tecnlogia da Informação(GTI).

## 📋 Sobre o Projeto

Este dashboard permite explorar e analisar três datasets relacionados à saúde mental:
- **Dataset Principal**: Dados gerais sobre saúde mental no trabalho
- **Dataset Burnout**: Análise específica de níveis de estresse e burnout
- **Dataset Workplace**: Informações sobre trabalho remoto e ambiente de trabalho

## ✨ Funcionalidades

### 📊 Visualizações Interativas
- Gráficos Plotly totalmente interativos (zoom, hover, seleção)
- Visualizações premium com estilo enterprise
- Heatmaps de risco e distribuições estatísticas

### 🎯 Filtros Dinâmicos
- Filtro por cargo/ocupação
- Filtro por modalidade de trabalho (remoto, híbrido, presencial)
- Filtro por carga horária semanal
- Filtro por segmentos/departamentos (em páginas específicas)

### 📈 Métricas e KPIs
- Indicadores globais em tempo real
- Comparações entre grupos
- Análise de tendências

### 📱 Interface
- Layout responsivo e intuitivo
- Tema dark configurável
- Navegação multipágina fluida
- Tooltips e ajuda contextual nos filtros

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
git clone https://github.com/seu-usuario/mental-health-dashboard.git
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
- No Windows OU macOS/Linux : você verá `(venv)` no início do prompt


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

O dashboard possui 6 páginas principais:

1. **🧠 Visão Geral** (`1_Visao_Geral.py`) - Página inicial com indicadores globais
2. **🔥 Burnout** - Análise detalhada de níveis de estresse e burnout
3. **🏢 Ambiente de Trabalho** - Impacto das políticas organizacionais
4. **🏠 Remoto & Híbrido** - Comparação entre modalidades de trabalho
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

**Dica**: Comece pela página "Visão Geral" para ter uma visão completa dos dados antes de explorar análises específicas.

## 📁 Estrutura do Projeto

```
mental-health-dashboard/
├── 1_Visao_Geral.py          # 🏠 Arquivo principal - execute este para iniciar
├── pages/                     # 📄 Páginas adicionais do dashboard
│   ├── 2_Burnout.py          # Análise de burnout
│   ├── 3_Ambiente_Trabalho.py
│   ├── 4_Remoto_Hibrido.py
│   ├── 5_Perfis_Segmentos.py
│   └── 6_Sobre_Metodos.py
├── data/                      # 📊 Datasets CSV (obrigatórios)
│   ├── dataset_principal.csv
│   ├── dataset_burnout.csv
│   └── dataset_workplace.csv
├── utils/                     # 🛠️ Utilitários e funções auxiliares
│   ├── data_io.py            # Carregamento e normalização de dados
│   ├── charts.py             # Funções de visualização
│   └── theming.py            # Configurações de tema
├── insights/                  # 💡 Módulos de análise e insights
│   ├── burnout.py
│   ├── enviroments.py
│   ├── modalidades.py
│   ├── overview.py
│   └── segments.py
├── ui/                        # 🎨 Componentes de interface
│   └── insight_box.py
├── .streamlit/                # ⚙️ Configurações do Streamlit
│   ├── config.toml           # Tema e configurações visuais
│   └── secrets.toml.example  # Template para variáveis secretas
├── venv/                      # 🐍 Ambiente virtual Python (gerado localmente)
├── requirements.txt           # 📦 Lista de dependências
├── .gitignore                # Arquivos ignorados pelo Git
├── LICENSE                   # Licença MIT
└── README.md                 # Este arquivo
```

**Arquivos importantes:**
- `1_Visao_Geral.py`: Execute este arquivo para iniciar o dashboard
- `data/*.csv`: Os datasets são carregados automaticamente pelo dashboard
- `requirements.txt`: Contém todas as dependências necessárias

## 📊 Datasets

Os datasets utilizados contêm informações sobre:

- **Demographics**: Gênero, idade, localização
- **Work Environment**: Tipo de trabalho, ambiente, carga horária
- **Mental Health**: Níveis de estresse, burnout, satisfação
- **Remote Work**: Dados sobre trabalho remoto e híbrido

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

### Passo 2: Acesse o Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"

### Passo 3: Configure o deploy

1. Selecione o repositório: `seu-usuario/mental-health-dashboard`
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

- **[Streamlit](https://streamlit.io/)** - Framework para criação de dashboards
- **[Pandas](https://pandas.pydata.org/)** - Manipulação e análise de dados
- **[Plotly](https://plotly.com/)** - Visualizações interativas
- **[NumPy](https://numpy.org/)** - Computação numérica
- **[Matplotlib](https://matplotlib.org/)** - Visualizações estáticas
- **[Seaborn](https://seaborn.pydata.org/)** - Visualizações estatísticas
- **[Statsmodels](https://www.statsmodels.org/)** - Modelagem estatística

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- Bruno Maciel - [@Bruno-fmaciel](https://github.com/Bruno-fmaciel)
- Camila Oliveira -[@camilamariaoliveira](https://github.com/camilamariaoliveira)

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub ou entre em contato com os autores.