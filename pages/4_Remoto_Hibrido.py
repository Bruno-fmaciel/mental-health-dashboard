import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.charts import violin_by_workmode

st.set_page_config(page_title="Remoto & Híbrido — SR2", page_icon="🏠", layout="wide")

st.title("🏠 Remoto & Híbrido")
df = load_data()
df = render_sidebar(df)

st.subheader("Distribuições por modalidade de trabalho")
st.plotly_chart(violin_by_workmode(df), use_container_width=True, key="violin_by_workmode")

st.info("TODO: adicionar deltas de risco por modalidade e segmentos (gênero, idade, região).")

