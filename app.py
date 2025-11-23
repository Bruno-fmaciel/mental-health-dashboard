import streamlit as st
import pandas as pd
from utils.data_io import load_data, render_sidebar
from utils.theming import set_page_theme
from utils.charts import kpi_cards, dist_stress

# Configuracao basica da pagina
st.set_page_config(
    page_title="Mental Health — Dashboard SR2",
    page_icon="🧠",
    layout="wide"
)
set_page_theme()

# Carrega dados
df = load_data()

# Sidebar global (filtros compartilhados)
filtered = render_sidebar(df)

# ====================================
# TITULO E CONTEXTO
# ====================================
st.title("🧠 Saude Mental no Ambiente de Trabalho")
st.caption("Dashboard Interativo • Grupo 6 - Projetos 5 - 2025.2 - GTI - SR2")

st.markdown("""
<div style='background-color: rgba(42, 42, 42, 0.3); padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #4A90E2; margin-bottom: 2rem;'>

### O Problema

O **burnout** e outros transtornos relacionados ao trabalho afetam milhoes de profissionais globalmente. 
Fatores como **carga horaria excessiva**, **falta de suporte organizacional** e **modalidade de trabalho** 
impactam diretamente o bem-estar e a produtividade dos colaboradores.

### Objetivo deste Dashboard

Este dashboard analisa dados de **saude mental no ambiente corporativo** para:
- Identificar **segmentos de alto risco** (departamentos, cargos, regioes)
- Comparar o impacto de **politicas organizacionais** e **modalidades de trabalho**
- Fornecer **insights acionaveis** para intervencoes preventivas

Use os filtros na sidebar para explorar diferentes perfis e descobrir padroes ocultos nos dados.

</div>
""", unsafe_allow_html=True)

st.divider()

# ====================================
# INDICADORES-CHAVE GLOBAIS
# ====================================
st.subheader("📊 Panorama Geral")
st.caption("Indicadores calculados sobre os dados filtrados na sidebar. Explore os filtros para segmentar a analise.")

kpi_cards(filtered)

st.divider()

# ====================================
# COMO NAVEGAR
# ====================================
st.subheader("🗺️ Como Navegar pelo Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 📍 Rota Sugerida
    
    1. **Visao Geral** - Comece aqui para ver o panorama geral dos indicadores
    2. **Burnout** - Entenda como carga de trabalho e cargo afetam o estresse
    3. **Ambiente de Trabalho** - Compare politicas de suporte e seu impacto no bem-estar
    """)

with col2:
    st.markdown("""
    #### 📍 Analises Avancadas
    
    4. **Remoto & Hibrido** - Compare diferencas entre modalidades de trabalho
    5. **Perfis & Segmentos** - Identifique grupos criticos que precisam de atencao
    6. **Sobre & Metodos** - Entenda a metodologia e fontes de dados utilizadas
    """)

st.info("""
💡 **Dica**: Use os **filtros na sidebar** para segmentar a analise por cargo, modalidade de trabalho, 
horas semanais e departamento. Cada pagina reflete os filtros aplicados, permitindo analises personalizadas.
""")

st.divider()

# ====================================
# DISTRIBUICAO DE ESTRESSE (AMOSTRA)
# ====================================
st.subheader("📈 Distribuicao de Estresse na Amostra")
st.caption("Visualize como o estresse esta distribuido entre os respondentes. Valores acima de 6 indicam alto estresse.")

st.plotly_chart(dist_stress(filtered), use_container_width=True, key="dist_stress_home")

st.divider()

# ====================================
# FOOTER
# ====================================
col_footer1, col_footer2 = st.columns([2, 1])

with col_footer1:
    st.caption("""
    **Dashboard desenvolvido para**: Projetos 5 - GTI - SR2  
    **Fontes de dados**: 3 datasets integrados (saude mental geral, burnout, trabalho remoto)  
    **Tecnologias**: Python, Streamlit, Plotly, Pandas
    """)

with col_footer2:
    st.caption("""
    **Comece a explorar** navegando pelas paginas no menu lateral →
    """)
