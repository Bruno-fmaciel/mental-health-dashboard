import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.charts import stacked_env_policies

st.set_page_config(page_title="Ambiente de Trabalho — SR2", page_icon="🏢", layout="wide")

st.title("🏢 Ambiente de Trabalho")
df = load_data()
df = render_sidebar(df)

st.subheader("Políticas/Condições × Resultado de Saúde Mental")
st.plotly_chart(stacked_env_policies(df), use_container_width=True, key="stacked_env_policies")

st.info("TODO: selecione até 3 políticas/variáveis ambientais chave para reduzir ruído.")

