# 🧠 Dashboard de Saúde Mental no Trabalho

Dashboard interativo desenvolvido em Streamlit para análise e visualização de dados relacionados à saúde mental no ambiente de trabalho. Este projeto foi desenvolvido como parte do SR2 de Projetos 5.

## 📋 Sobre o Projeto

Este dashboard permite explorar e analisar três datasets relacionados à saúde mental:
- **Dataset Principal**: Dados gerais sobre saúde mental no trabalho
- **Dataset Burnout**: Análise específica de níveis de estresse e burnout
- **Dataset Workplace**: Informações sobre trabalho remoto e ambiente de trabalho

## ✨ Funcionalidades

- Visualizações interativas com Plotly
- Métricas e KPIs em tempo real
- Análise de distribuição de dados
- Interface responsiva e intuitiva
- Navegação multipágina

## 🔧 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

## 🚀 Instalação e Execução Local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/mental-health-dashboard.git
cd mental-health-dashboard
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o dashboard

```bash
streamlit run 1_Visao_Geral.py
```

O dashboard será aberto automaticamente no seu navegador em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
mental-health-dashboard/
├── app.py                      # Página principal do dashboard
├── pages/                      # Páginas adicionais
│   └── 2_Burnout.py           # Análise de burnout
├── data/                       # Datasets
│   ├── dataset_principal.csv
│   ├── dataset_burnout.csv
│   └── dataset_workplace.csv
├── .streamlit/                 # Configurações do Streamlit
│   ├── config.toml            # Configurações de tema e servidor
│   └── secrets.toml.example   # Template para secrets
├── requirements.txt            # Dependências do projeto
├── .gitignore                 # Arquivos ignorados pelo Git
├── LICENSE                    # Licença MIT
└── README.md                  # Este arquivo
```

## 📊 Datasets

Os datasets utilizados contêm informações sobre:

- **Demographics**: Gênero, idade, localização
- **Work Environment**: Tipo de trabalho, ambiente, carga horária
- **Mental Health**: Níveis de estresse, burnout, satisfação
- **Remote Work**: Dados sobre trabalho remoto e híbrido

## 🌐 Deploy no Streamlit Cloud

### Passo 1: Prepare o repositório

Certifique-se de que todos os arquivos necessários estão commitados:
- `app.py`
- `requirements.txt`
- Pasta `data/` com os datasets
- Pasta `pages/` com as páginas adicionais

### Passo 2: Acesse o Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"

### Passo 3: Configure o deploy

1. Selecione o repositório: `seu-usuario/mental-health-dashboard`
2. Branch: `main` ou `developer`
3. Main file path: `app.py`
4. Clique em "Deploy!"

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
- Camila Oliveira

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub ou entre em contato com os autores.

---

Desenvolvido com ❤️ para o SR2 de Projetos 5