import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.theming import set_page_theme
from utils.charts import kpi_cards
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

# Validação de DataFrame vazio
if filtered.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

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
        Panorama geral de estresse, burnout e carga horária no ambiente de trabalho. 
        Explore padrões, identifique grupos de risco e apoie decisões baseadas em dados.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ============================
# KPIs — PAINEL PRINCIPAL
# ============================
st.subheader("📊 Indicadores Globais")
st.caption("Panorama geral dos principais indicadores. Use os filtros na barra lateral para explorar diferentes grupos e identificar padrões de risco.")

kpi_cards(filtered, df)

st.markdown("<br>", unsafe_allow_html=True)

# ============================
# GRÁFICOS 
# ============================
st.subheader("📈 Insights Visuais")

col1, col2 = st.columns(2)

# --- GRÁFICO 1: DISTRIBUIÇÃO DE ESTRESSE ---
with col1:
    st.markdown("#### 😰 Distribuição de Estresse")
    st.caption("Distribuição do nível de estresse no conjunto de dados. Valores mais altos indicam maior estresse relatado.")
    st.plotly_chart(stress_distribution_premium(filtered), use_container_width=True)

# --- GRÁFICO 2: HORAS × ESTRESSE ---
with col2:
    st.markdown("#### ⏰ Carga Horária × Estresse")
    st.caption("Relação entre horas trabalhadas por semana e nível de estresse. Neste conjunto de dados, observe se há associação entre essas variáveis.")
    st.plotly_chart(hours_vs_stress_premium(filtered), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


# ============================
# SEGMENTOS
# ============================
if "segment" in filtered.columns and "burnout_level" in filtered.columns:
    st.subheader("🔥 Análise de Segmentos Críticos")
    st.caption("Comparação dos segmentos com maior risco de burnout. Segmentos com maior percentual de burnout alto requerem atenção prioritária.")

    st.plotly_chart(
        burnout_segments_premium(filtered),
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

# ============================
# HEATMAP DE RISCO
# ============================
if "work_mode" in filtered.columns:
    st.subheader("🌡 Heatmap de Correlações")
    st.caption("Mapa de correlações entre indicadores numéricos. Valores próximos de +1 ou -1 indicam associações mais fortes neste conjunto de dados.")

    st.plotly_chart(
        risk_heatmap_premium(filtered),
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================
# FOOTER
# ============================
st.markdown("<br><hr><center style='color:gray'>Dashboard • Projetos 5 — GTI • 2025</center>",
            unsafe_allow_html=True)
