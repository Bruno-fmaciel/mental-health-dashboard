import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_io import load_data, render_sidebar
from utils.charts import scatter_hours_burnout, box_burnout_by_role

st.set_page_config(page_title="Burnout — SR2", page_icon="🔥", layout="wide")


st.title("🔥 Análise do Dataset Burnout")

df = pd.read_csv("data/dataset_burnout.csv")

st.write("Visualização rápida dos dados:")
st.dataframe(df.head())

if "Stress_Level" in df.columns:
    fig = px.histogram(df, x="Stress_Level", title="Distribuição do Nível de Estresse")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Coluna 'Stress_Level' não encontrada.")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Horas de trabalho × Burnout")
    st.plotly_chart(scatter_hours_burnout(df), use_container_width=True, key="scatter_hours_burnout")
with c2:
    st.subheader("Burnout por cargo/modalidade")
    st.plotly_chart(box_burnout_by_role(df), use_container_width=True, key="box_burnout_by_role")