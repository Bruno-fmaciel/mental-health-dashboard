import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🔥 Análise do Dataset Burnout")

df = pd.read_csv("data/dataset_burnout.csv")

st.write("Visualização rápida dos dados:")
st.dataframe(df.head())

if "Stress_Level" in df.columns:
    fig = px.histogram(df, x="Stress_Level", title="Distribuição do Nível de Estresse")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Coluna 'Stress_Level' não encontrada.")