import streamlit as st

st.set_page_config(page_title="Sobre & Métodos — SR2", page_icon="ℹ️", layout="wide")

st.title("ℹ️ Sobre & Métodos")

st.markdown("""
### 🎯 Problema & Perguntas de Negócio

**Problema**: 
TODO: Descreva o problema de negócio que o dashboard aborda.

*Exemplo*: Como a transição para trabalho remoto/híbrido impactou a saúde mental 
dos trabalhadores? Quais fatores organizacionais podem mitigar o burnout?

**Perguntas de Pesquisa**:
1. TODO: Primeira pergunta que o dashboard responde
2. TODO: Segunda pergunta que o dashboard responde
3. TODO: Terceira pergunta que o dashboard responde
4. TODO: Quarta pergunta que o dashboard responde (opcional)
5. TODO: Quinta pergunta que o dashboard responde (opcional)

*Sugestões*:
- Qual a prevalência de burnout entre diferentes modalidades de trabalho?
- Horas trabalhadas influenciam o nível de estresse?
- O acesso a recursos de saúde mental reduz o burnout?
- Quais indústrias/regiões apresentam maior risco?

---

### 📊 Dados & Preparação

**Fontes dos Dados**:

TODO: Descreva as fontes dos dados

*Template*:
- **Dataset Principal**: Pesquisa de saúde mental no trabalho 
  - Tamanho: [número] respondentes
  - Período: [ano/período]
  
- **Dataset Burnout**: Estudo sobre burnout em trabalho remoto
  - Tamanho: [número] respondentes
  - Período: [ano/período]
  
- **Dataset Workplace**: Dados de satisfação e ambiente organizacional
  - Tamanho: [número] respondentes
  - Período: [ano/período]

**Limpeza e Tratamento**:

TODO: Descreva o processo de limpeza dos dados

*Processos aplicados*:
- Normalização de colunas entre datasets (role, work_mode, stress_score)
- Mapeamento de stress categórico para numérico (Low=2, Medium=5, High=8)
- Criação de variável burnout_level (categorização em low/medium/high)
- Remoção de valores ausentes em variáveis-chave
- TODO: Adicione outros processos específicos do seu projeto

**Limitações**:

TODO: Liste as limitações dos dados e análises

*Exemplo*:
- Dados auto-reportados (possível viés de resposta)
- Datasets de fontes diferentes (possível inconsistência temporal)
- Não há informações longitudinais (impossível inferir causalidade)
- Amostra pode não ser representativa de todas as indústrias

---

### 🔬 Metodologias

#### CRISP-DM (Cross-Industry Standard Process for Data Mining)
1. **Entendimento do Negócio**: Identificação do problema de saúde mental no trabalho
2. **Entendimento dos Dados**: Exploração dos 3 datasets e suas características
3. **Preparação dos Dados**: Limpeza, normalização e integração dos datasets
4. **Modelagem/Visualização**: Criação de gráficos interativos e análises
5. **Avaliação**: Validação das análises com o time e stakeholders
6. **Implantação**: Deploy do dashboard no Streamlit Cloud

#### Storytelling com Dados
- Estrutura narrativa: cada página conta uma parte da história
- Gráficos com títulos que respondem "o que vejo?"
- Uso de anotações e destaques para insights principais
- Cores consistentes (burnout alto = vermelho, baixo = verde)
- Foco em insights acionáveis

#### Design de Dashboards
- **Foco no usuário**: Filtros interativos para exploração
- **Hierarquia visual**: KPIs no topo, detalhes abaixo
- **Contexto**: Comparações entre segmentos e modalidades
- **Interatividade**: Gráficos Plotly com hover e zoom
- **Responsividade**: Layout adaptável (wide mode)

---

### 👥 Time & Artefatos

**Equipe**:
- Bruno Maciel ([@Bruno-fmaciel](https://github.com/Bruno-fmaciel))
- Camila Oliveira
- TODO: Adicione outros membros do time

**Artefatos do Projeto**:
""")

# Links clicáveis
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🔗 Links Principais
    - **Repositório GitHub**: [Ver código](https://github.com/Bruno-fmaciel/mental-health-dashboard)
    - **Dashboard**: TODO - Adicionar após deploy
    - **Slides**: TODO - Adicionar link
    """)

with col2:
    st.markdown("""
    #### 📚 Recursos
    - **Google Site**: TODO - Adicionar link
    - **Documentação**: Ver README no repo
    - **Licença**: MIT License
    """)

st.divider()

st.markdown("""
### 📖 Referências

TODO: Adicione as referências bibliográficas utilizadas

*Sugestões*:
- Fontes dos datasets
- Artigos sobre burnout e saúde mental
- Documentação das ferramentas (Streamlit, Plotly, etc.)
- Metodologias (CRISP-DM, Storytelling com Dados)
""")

st.info("💡 **Dica**: Atualize esta página conforme o projeto evolui. Ela é essencial para o SR2!")

