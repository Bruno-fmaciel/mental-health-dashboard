import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.theming import set_page_theme
from utils.charts import (
    make_burnout_kpi_cards,
    plot_hours_vs_stress_scatter,
    plot_stress_by_hours_band,
    plot_roles_burnout_ranking
)

st.set_page_config(page_title="Burnout — SR2", page_icon="🔥", layout="wide")
set_page_theme()

# ====================================
# CARREGA E FILTRA DADOS
# ====================================
df = load_data()
df_filtered = render_sidebar(df)

# Verifica se há dados após filtros
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Ajuste os filtros na sidebar.")
    st.stop()

# ====================================
# HERO SECTION
# ====================================
st.title("Burnout & carga de trabalho")
st.caption("Associação entre intensidade de trabalho e risco de estresse e burnout.")

# ====================================
# KPIs (3 COLUMNS)
# ====================================
burnout_high_pct, stress_mean, hours_mean = make_burnout_kpi_cards(df_filtered)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("% Burnout Alto", f"{burnout_high_pct:.1f}%")

with col2:
    st.metric("Estresse Médio", f"{stress_mean:.1f}")

with col3:
    st.metric("Horas/Semana", f"{hours_mean:.1f}h")

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 1: MAIN CHART (FULL-WIDTH SCATTER)
# ====================================
st.plotly_chart(plot_hours_vs_stress_scatter(df_filtered), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 2: STRESS BY HOURS BAND
# ====================================
st.plotly_chart(plot_stress_by_hours_band(df_filtered), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 3: ROLES BURNOUT RANKING
# ====================================
st.plotly_chart(plot_roles_burnout_ranking(df_filtered), use_container_width=True)

# ====================================
# FOOTER
# ====================================
st.markdown("<br><hr><center style='color:gray'>Dashboard • Projetos 5 — GTI • 2025</center>",
            unsafe_allow_html=True)
