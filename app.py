import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Saúde Mental",
    layout="wide",
    page_icon="🧠"
)

st.title("🧠 Dashboard de Saúde Mental no Trabalho")

# --- Carregar os datasets ---
@st.cache_data
def carregar_dados():
    df_principal = pd.read_csv("data/dataset_principal.csv")
    df_burnout = pd.read_csv("data/dataset_burnout.csv")
    df_remote = pd.read_csv("data/dataset_workplace.csv")
    return df_principal, df_burnout, df_remote

df_principal, df_burnout, df_remote = carregar_dados()

# --- Mostrar métricas iniciais ---
col1, col2, col3 = st.columns(3)
col1.metric("Registros (Principal)", len(df_principal))
col2.metric("Registros (Burnout)", len(df_burnout))
col3.metric("Registros (Remoto)", len(df_remote))

# --- Gráfico de exemplo ---
st.subheader("Distribuição de gênero - Dataset Principal")
if "Gender" in df_principal.columns:
    graf = px.histogram(df_principal, x="Gender", title="Distribuição de Gênero")
    st.plotly_chart(graf, use_container_width=True)
else:
    st.warning("Coluna 'Gender' não encontrada no dataset principal.")