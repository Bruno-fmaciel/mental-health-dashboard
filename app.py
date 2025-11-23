# app.py
import streamlit as st
import pandas as pd
from utils.charts import kpi_cards, stacked_env_policies, small_multiples_segments

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Dashboard de Saúde Mental no Trabalho",
    layout="wide",
)

# ===============================
# ESTILO GLOBAL
# ===============================
st.markdown("""
    <style>
        /* Remove padding lateral padrão */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* Títulos e subtítulos */
        h1, h2, h3 {
            font-weight: 600 !important;
            color: #E4E6EB !important;
        }

        /* Métricas (KPIs) */
        [data-testid="stMetricValue"] {
            color: #2980b9;
            font-weight: 600;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #111418 !important;
            border-right: 1px solid #2b2b2b;
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
# TÍTULO E INTRODUÇÃO
# ===============================
st.title("Dashboard de Saúde Mental no Trabalho")
st.caption("Análise integrada de fatores de estresse, burnout e produtividade entre diferentes perfis e ambientes de trabalho.")

st.markdown("---")

# ===============================
# CARREGAMENTO DOS DADOS
# ===============================
@st.cache_data
def carregar_dados():
    df_main = pd.read_csv("data/dataset_principal.csv")
    df_burnout = pd.read_csv("data/dataset_burnout.csv")
    df_remote = pd.read_csv("data/dataset_workplace.csv")
    return df_main, df_burnout, df_remote

df_main, df_burnout, df_remote = carregar_dados()

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("Configurações")
opcao = st.sidebar.selectbox(
    "Selecione o conjunto de dados:",
    ("Principal", "Burnout", "Remote")
)

# ===============================
# SELEÇÃO DE DATASET
# ===============================
if opcao == "Principal":
    st.subheader("Dataset Principal — Saúde Mental Geral")
    st.info("Inclui hábitos, histórico de saúde mental e fatores relacionados ao estresse.")
    df = df_main
elif opcao == "Burnout":
    st.subheader("Dataset Burnout — Esgotamento Profissional")
    st.info("Mede produtividade, estresse e recursos organizacionais disponíveis.")
    df = df_burnout
else:
    st.subheader("Dataset Remote — Trabalho Remoto e Híbrido")
    st.info("Analisa produtividade, equilíbrio vida-trabalho e suporte psicológico no trabalho remoto.")
    df = df_remote

st.markdown("---")

# ===============================
# KPIs
# ===============================
st.markdown("### Indicadores-Chave")
kpi_cards(df, title=None)

st.markdown("---")

# ===============================
# POLÍTICAS E SUPORTE
# ===============================
st.markdown("### Políticas e Recursos Organizacionais")
try:
    fig_policies = stacked_env_policies(df, normalize=True)
    st.plotly_chart(fig_policies, use_container_width=True)
except Exception as e:
    st.warning(f"Não foi possível gerar gráfico de políticas: {e}")

st.markdown("---")

# ===============================
# SEGMENTOS E TENDÊNCIAS
# ===============================
st.markdown("### Tendências por Segmento")
try:
    fig_segments = small_multiples_segments(df, top_n=8)
    st.plotly_chart(fig_segments, use_container_width=True)
except Exception as e:
    st.warning(f"Não foi possível gerar gráfico de segmentos: {e}")

# ===============================
# TABELA DE AMOSTRA
# ===============================
st.markdown("---")
st.markdown("### Amostra de Dados")
st.dataframe(df.head(10), use_container_width=True)
