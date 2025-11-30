import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.theming import set_page_theme
from utils.charts import (
    make_overview_kpi_cards,
    plot_stress_distribution_histogram,
    plot_burnout_level_composition,
    plot_core_correlation_heatmap
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
# HERO SECTION
# ============================
st.title("Panorama da Saúde Mental")
st.caption("Resumo geral de estresse, burnout e carga de trabalho neste conjunto de dados.")

# ============================
# KPIs ROW
# ============================
n, stress_mean, burnout_high_pct, hours_mean = make_overview_kpi_cards(filtered)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Respondentes", f"{n:,}")

with col2:
    st.metric("Estresse Médio", f"{stress_mean:.1f}")

with col3:
    st.metric("% Burnout Alto", f"{burnout_high_pct:.1f}%")

with col4:
    st.metric("Horas/Semana", f"{hours_mean:.1f}h")

st.markdown("<br>", unsafe_allow_html=True)

# ============================
# BLOCK 1: TWO COLUMNS
# ============================
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(plot_stress_distribution_histogram(filtered), use_container_width=True)

with col2:
    st.plotly_chart(plot_burnout_level_composition(filtered), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================
# BLOCK 2: FULL-WIDTH HEATMAP
# ============================
st.plotly_chart(plot_core_correlation_heatmap(filtered), use_container_width=True)

# ============================
# FOOTER
# ============================
st.markdown("<br><hr><center style='color:gray'>Dashboard • Projetos 5 — GTI • 2025</center>",
            unsafe_allow_html=True)
