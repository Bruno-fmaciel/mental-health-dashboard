import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.charts import kpi_cards, dist_stress

st.set_page_config(page_title="Visão Geral — SR2", page_icon="📊", layout="wide")

st.title("📊 Visão Geral")
df = load_data()
df = render_sidebar(df)

# KPIs principais (ajuste métricas no utils/charts.py)
kpi_cards(df)

st.subheader("Distribuição de Estresse/Índice de Risco")
st.plotly_chart(dist_stress(df), use_container_width=True, key="dist_stress_visao_geral")

st.info("TODO: adicionar 1–2 gráficos adicionais que respondam às perguntas de negócio.")

