import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.theming import set_page_theme
from utils.charts import (
    make_environment_kpi_cards,
    plot_burnout_distribution_by_policy,
    plot_policy_burnout_ranking,
    make_policy_summary_table
)

st.set_page_config(page_title="Ambiente de Trabalho — SR2", page_icon="🏢", layout="wide")
set_page_theme()

# ====================================
# CARREGA E FILTRA DADOS
# ====================================
df = load_data()
df_filtered = render_sidebar(df)

# Verifica se há dados
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Ajuste os filtros na sidebar.")
    st.stop()

# ====================================
# HERO SECTION
# ====================================
st.title("Ambiente & políticas organizacionais")
st.caption("Comparação de políticas de trabalho em termos de risco de burnout.")

# ====================================
# KPIs
# ====================================
n_policies, burnout_high_pct, stress_mean = make_environment_kpi_cards(df_filtered)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Políticas Distintas", n_policies)

with col2:
    st.metric("% Burnout Alto", f"{burnout_high_pct:.1f}%")

with col3:
    st.metric("Estresse Médio", f"{stress_mean:.1f}")

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 1: MAIN CHART (BURNOUT DISTRIBUTION BY POLICY)
# ====================================
st.plotly_chart(plot_burnout_distribution_by_policy(df_filtered), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 2: RANKING CHART
# ====================================
st.plotly_chart(plot_policy_burnout_ranking(df_filtered), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 3: OPTIONAL TABLE
# ====================================
summary_df = make_policy_summary_table(df_filtered)
if not summary_df.empty:
    st.subheader("Resumo por política")
    st.dataframe(summary_df, use_container_width=True)

# ====================================
# FOOTER
# ====================================
st.markdown("<br><hr><center style='color:gray'>Dashboard • Projetos 5 — GTI • 2025</center>",
            unsafe_allow_html=True)
