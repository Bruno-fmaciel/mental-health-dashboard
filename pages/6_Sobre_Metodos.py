import streamlit as st
import pandas as pd
from utils.data_io import load_data
from utils.theming import set_page_theme

st.set_page_config(
    page_title="Sobre & Métodos — SR2",
    page_icon="ℹ️",
    layout="wide"
)
set_page_theme()

# ====================================
# HERO SECTION
# ====================================
st.title("Sobre & métodos")
st.caption("Contexto, dados e passos usados para construir este dashboard.")

# ====================================
# PROBLEM & QUESTIONS
# ====================================
with st.container():
    st.subheader("Problema & perguntas")
    st.markdown("""
    - Organizações enfrentam aumento de estresse e burnout no trabalho
    - Identificar grupos de risco e fatores organizacionais influentes
    - Quais segmentos apresentam maior risco?
    - A carga horária influencia o estresse?
    - Modalidade de trabalho impacta o bem-estar?
    - Políticas organizacionais estão associadas a menor risco?
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# DATA & PREPARATION
# ====================================
with st.container():
    st.subheader("Dados & preparação")
    st.markdown("""
    - `dataset_principal.csv` — saúde mental, hábitos e características individuais
    - `dataset_burnout.csv` — níveis de estresse e burnout
    - `dataset_workplace.csv` — modalidades de trabalho, satisfação, políticas
    - Normalização de `work_mode` → remoto / híbrido / presencial
    - Padronização de cargos e segmentos
    - Conversão de estresse para escala 0–10
    - Criação da variável categórica `burnout_level`
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# METHOD STEPS
# ====================================
with st.container():
    st.subheader("Passos metodológicos")
    st.markdown("""
    1. Entendimento do negócio
    2. Entendimento dos dados
    3. Preparação da base integrada
    4. Modelagem visual (dashboards e KPIs)
    5. Avaliação de hipóteses
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# LIMITATIONS & CARE
# ====================================
with st.container():
    st.subheader("Limitações & cuidados")
    st.markdown("""
    - Dados auto-reportados → viés de percepção
    - Diferenças de estrutura entre datasets
    - Amostras pequenas em alguns segmentos
    - Não há dados longitudinais (não medimos mudança no tempo)
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# TEAM / TOOLS
# ====================================
with st.container():
    st.subheader("Equipe & ferramentas")
    st.markdown("""
    - Equipe: Bruno Maciel, Camila Oliveira, Maria Clara Medeiros, Yuri Tavares, Rodrigo Lyra, Artur Tavares
    - Ferramentas: Streamlit, Plotly Express, Pandas
    - Projeto: SR2 — Projetos 5 — GTI — 2025
    """)

# ====================================
# FOOTER
# ====================================
st.markdown("<br><hr><center style='color:gray'>Dashboard • Projetos 5 — GTI • 2025</center>",
            unsafe_allow_html=True)
