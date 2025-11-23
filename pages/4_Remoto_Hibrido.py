import streamlit as st
import pandas as pd
from utils.data_io import load_data, render_sidebar
import plotly.express as px
from ui.insight_box import insight_box
from insights.modalidades import insights_modalidades


st.set_page_config(layout="wide", page_title="Modalidades de Trabalho")

df = load_data()
filtered = render_sidebar(df)

st.title("🏠 Comparação entre Modalidades de Trabalho")
st.caption("Análise entre trabalho presencial, remoto e híbrido conforme os dados filtrados.")

st.divider()

# ============================
# KPIs por modalidade
# ============================
st.subheader("📊 Indicadores por Modalidade")

group_cols = ["stress_score", "hours_per_week"]

if "work_mode" not in filtered.columns:
    st.error("A coluna 'work_mode' não existe no dataframe final. Verifique load_data().")
    st.stop()

modalidade_stats = (
    filtered
    .groupby("work_mode")[group_cols]
    .mean()
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        modalidade_stats,
        x="work_mode",
        y="stress_score",
        title="Estresse Médio por Modalidade",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        modalidade_stats,
        x="work_mode",
        y="hours_per_week",
        title="Horas Semanais Médias por Modalidade",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ============================
# Distribuição de Estresse
# ============================
st.subheader("📈 Distribuição de Estresse por Modalidade")

fig = px.box(
    filtered,
    x="work_mode",
    y="stress_score",
    title="Distribuição de Estresse"
)
st.plotly_chart(fig, use_container_width=True)

insights = insights_modalidades(filtered)
formatted = "<ul>" + "".join([f"<li>{i}</li>" for i in insights]) + "</ul>"

insight_box(
    title="🏠 Insights Automáticos: Modalidades de Trabalho",
    content=formatted
)

