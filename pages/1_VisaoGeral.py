# pages/1_Visao_Geral.py
import streamlit as st
import pandas as pd
from utils.charts import kpi_cards, small_multiples_segments

# ===============================
# CONFIGURAÇÃO
# ===============================
st.set_page_config(layout="wide")

st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        h1, h2, h3 {
            font-weight: 600 !important;
            color: #E4E6EB !important;
        }

        [data-testid="stMetricValue"] {
            color: #2980b9;
            font-weight: 600;
        }

        section[data-testid="stSidebar"] {
            background-color: #111418 !important;
        }

        .intro-box {
            background-color: #1B1F24;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border: 1px solid #2a2a2a;
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
# TÍTULO E INTRODUÇÃO
# ===============================
st.title("Visão Geral do Projeto")
st.caption("Análise de saúde mental, estresse e produtividade em diferentes contextos de trabalho")

st.markdown("""
<div class='intro-box'>
<b>Objetivo:</b> compreender como fatores organizacionais, padrões de trabalho e hábitos individuais influenciam
o bem-estar e a produtividade de profissionais em diferentes ambientes — presenciais, híbridos e remotos.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===============================
# DADOS E KPI GERAIS
# ===============================
@st.cache_data
def carregar_dados():
    df_main = pd.read_csv("data/dataset_principal.csv")
    df_burnout = pd.read_csv("data/dataset_burnout.csv")
    df_remote = pd.read_csv("data/dataset_workplace.csv")
    return df_main, df_burnout, df_remote

df_main, df_burnout, df_remote = carregar_dados()

st.markdown("### Indicadores Globais")

# KPIs gerais (combinação dos datasets)
df_all = pd.concat([df_main.assign(source="Principal"),
                    df_burnout.assign(source="Burnout"),
                    df_remote.assign(source="Remote")], ignore_index=True)

kpi_cards(df_all, title=None)

st.markdown("---")

# ===============================
# INSIGHTS INICIAIS
# ===============================
st.markdown("### Tendências Gerais por Contexto")

try:
    fig = small_multiples_segments(df_burnout, top_n=8, title="Média de Estresse/Burnout por Indústria (Dataset Burnout)")
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.warning(f"Não foi possível gerar o gráfico de tendências iniciais: {e}")

st.markdown("---")

# ===============================
# SEÇÃO DESCRITIVA
# ===============================
st.markdown("### Contexto dos Dados")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Dataset Principal**  
    - Inclui informações gerais de saúde mental, hábitos e suporte psicológico.  
    - Baseado em respostas individuais sobre fatores emocionais e comportamentais.  
    - Permite avaliar padrões de estresse e coping (lidar com situações adversas).  
    """)

    st.markdown("""
    **Dataset Burnout**  
    - Foco em trabalhadores presenciais e híbridos.  
    - Mede estresse, horas de trabalho e suporte organizacional.  
    - Inclui métricas de acesso a recursos de saúde mental e satisfação no trabalho.  
    """)

with col2:
    st.markdown("""
    **Dataset Remote**  
    - Concentra-se em trabalhadores remotos.  
    - Analisa produtividade, qualidade do sono e equilíbrio vida-trabalho.  
    - Inclui variáveis de suporte do gestor e recursos terapêuticos disponíveis.  
    """)

st.markdown("---")

# ===============================
# ENCERRAMENTO
# ===============================
st.markdown("""
<div class='intro-box'>
A integração desses três conjuntos de dados permite comparar padrões entre diferentes contextos
de trabalho e compreender de forma mais abrangente os fatores que influenciam o burnout,
a produtividade e o bem-estar psicológico.
</div>
""", unsafe_allow_html=True)
