import streamlit as st
import plotly.express as px
from utils.data_io import load_data, render_sidebar
from utils.theming import set_page_theme
from utils.charts import kpi_cards, dist_stress
from utils.charts import (
    stress_distribution_premium,
    hours_vs_stress_premium,
    burnout_segments_premium,
    risk_heatmap_premium
)

# ============================
# CONFIGURAÇÃO DA PÁGINA
# ============================
st.set_page_config(
    page_title="Mental Health Dashboard — SR2",
    page_icon="🧠",
    layout="wide"
)
set_page_theme()

# ============================
# CARREGA DADOS
# ============================
df = load_data()
filtered = render_sidebar(df)

# ============================
# HEADER — HERO SECTION
# ============================
st.markdown(
    """
<div style="
    padding: 20px 15px;
    border-radius: 14px;
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 2rem;
">
    <h1 style="margin: 0; font-size: 2.6rem; color: #4A90E2;">🧠 Saúde Mental no Trabalho</h1>
    <p style="color:#d1d5db; font-size:1.1rem; margin-top:8px;">
        Monitoramento integrado de estresse, burnout e condições de trabalho. 
        Explore tendências, identifique grupos de risco e apoie decisões baseadas em dados.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ============================
# KPIs — PAINEL PRINCIPAL
# ============================
st.subheader("📊 Indicadores Globais")

kpi_cards(filtered, df)

st.markdown("<br>", unsafe_allow_html=True)

# ============================
# GRÁFICOS 
# ============================
st.subheader("📈 Insights Visuais ")

col1, col2 = st.columns(2)

# --- GRÁFICO 1: DISTRIBUIÇÃO DE ESTRESSE ---
with col1:
    st.markdown("#### 😰 Distribuição de Estresse")
    st.plotly_chart(stress_distribution_premium(filtered), use_container_width=True)

# --- GRÁFICO 2: HORAS × ESTRESSE ---
with col2:
    st.markdown("#### ⏰ Carga Horária × Estresse")
    st.plotly_chart(hours_vs_stress_premium(filtered), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


# ============================
# SEGMENTOS
# ============================
if "segment" in filtered and "burnout_level" in filtered:
    st.subheader("🔥 Análise Segmentos Críticos")
    st.caption("Comparação direta dos segmentos com maior risco de burnout.")

    st.plotly_chart(
        burnout_segments_premium(filtered),
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

# ============================
# HEATMAP DE RISCO Visualização de risco cruzando modalide de trabalho e segmentos.
# ============================
if "work_mode" in filtered:
    st.subheader("🌡 Heatmap de Risco")

    st.plotly_chart(
        risk_heatmap_premium(filtered),
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================
# CALL TO ACTION — NAVEGAÇÃO
# ============================
st.success("""
### 🚀 Continue Explorando o Dashboard  
Use o menu lateral para análises aprofundadas:

- 🔥 **Burnout** — relação entre estresse e carga de trabalho  
- 🏢 **Ambiente de Trabalho** — impacto das políticas e condições organizacionais  
- 🏠 **Remoto & Híbrido** — comparação entre modalidades  
- 🧩 **Perfis & Segmentos** — identificação de grupos críticos  
- ℹ️ **Sobre & Métodos** — documentação completa do projeto  

Aproveite os filtros para conduzir sua análise durante a apresentação.
""")

# ============================
# FOOTER
# ============================
st.markdown("<br><hr><center style='color:gray'>Dashboard • Projetos 5 — GTI • 2025</center>",
            unsafe_allow_html=True)
