import streamlit as st
import pandas as pd
from utils.data_io import load_data
from utils.theming import set_page_theme

st.set_page_config(
    page_title="Sobre & Métodos",
    page_icon="ℹ️",
    layout="wide"
)
set_page_theme()

# ====================================
# HERO SECTION
# ====================================
st.title("Sobre & métodos")
# ====================================
# RESUMO AUTOMÁTICO
# ====================================

df = load_data()

if df is None or df.empty:
    st.warning("Não foi possível gerar o resumo automático. O dataset está vazio.")
else:
    total = len(df)
    stress_mean = df["stress_score"].mean()
    hours_mean = df["hours_per_week"].mean()
    
    if "burnout_level" in df.columns:
        pct_high = (df["burnout_level"].eq("high").mean() * 100)
    else:
        pct_high = None
    
    st.info(f"""
    ### 📝 Resumo da Base de Dados Utilizada
    
    - Total de respondentes integrados: **{total:,}**
    - Estresse médio geral: **{stress_mean:.2f}**
    - Horas semanais médias: **{hours_mean:.1f}h**
    - % de burnout alto: **{pct_high:.1f}%**  
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# PROBLEM & QUESTIONS
# ====================================
with st.container():
    st.subheader("🎯 Problema e Perguntas de Pesquisa")
    
    st.markdown("""
    **Problema central**
    
    Organizações enfrentam aumento de estresse e burnout no trabalho, mas carecem de visão integrada sobre *quem são os grupos de risco* e *quais fatores organizacionais mais influenciam esse cenário*.
    
    **Perguntas que guiam o projeto:**
    """)
    
    st.markdown("""
    1. Quais segmentos apresentam maior risco de burnout?
    2. A carga horária semanal influencia diretamente o estresse?
    3. Modalidade de trabalho (remoto/híbrido/presencial) impacta o bem-estar?
    4. Políticas organizacionais estão associadas a menor risco?
    5. Como diferentes dimensões (cargo, horas, departamento, política) interagem?
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# DATA & PREPARATION
# ====================================
with st.container():
    st.subheader("📊 Dados & Preparação")
    
    st.markdown("""
    **Fontes integradas no projeto:**
    """)
    
    st.markdown("""
    - `dataset_principal.csv` — saúde mental, hábitos e características individuais
    - `dataset_burnout.csv` — níveis de estresse e burnout
    - `dataset_workplace.csv` — modalidades de trabalho, satisfação, políticas
    """)
    
    st.markdown("""
    **Principais etapas de preparação:**
    """)
    
    st.markdown("""
    - Normalização de `work_mode` → remoto / híbrido / presencial
    - Padronização de cargos e segmentos
    - Conversão de estresse para escala 0–10
    - Criação da variável categórica `burnout_level`
    - Unificação dos 3 datasets com chaves compatíveis
    - Remoção de entradas inválidas e excesso de nulos
    """)
    
    st.markdown("""
    **Limitações da base:**
    """)
    
    st.markdown("""
    - Dados auto-reportados → viés de percepção
    - Diferenças de estrutura entre datasets
    - Amostras pequenas em alguns segmentos
    - Não há dados longitudinais (não medimos mudança no tempo)
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# METHOD STEPS
# ====================================
with st.container():
    st.subheader("🔬 Metodologias Utilizadas")
    
    st.markdown("""
    #### ✔ CRISP-DM (Adaptado)
    """)
    
    st.markdown("""
    1. Entendimento do negócio
    2. Entendimento dos dados
    3. Preparação da base integrada
    4. Modelagem visual (dashboards e KPIs)
    5. Avaliação de hipóteses
    6. Deploy (Streamlit Cloud)
    """)
    
    st.markdown("""
    #### ✔ Storytelling com Dados
    """)
    
    st.markdown("""
    - Títulos que comunicam a "mensagem" do gráfico
    - Comparações diretas entre grupos
    - Destaque a riscos e tendências
    - Priorização de KPIs no topo
    """)
    
    st.markdown("""
    #### ✔ Boas práticas de design de dashboards
    """)
    
    st.markdown("""
    - Layout horizontal (wide)
    - Gráficos interativos com Plotly Express
    - Uso consistente de cores semânticas
    - Cartões de KPI
    - Visualizações minimalistas (texto reduzido)
    """)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# TEAM / TOOLS / LINKS
# ====================================
with st.container():
    st.subheader("👥 Time & Artefatos do Projeto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Equipe:**
        
        - Bruno Maciel (Dev)
        - Camila Oliveira (Dev)
        - Maria Clara Medeiros
        - Yuri Tavares
        - Rodrigo Lyra
        - Artur Tavares
        
        **Código-fonte & Documentação:**
        
        - GitHub: [mental-health-dashboard](https://github.com/Bruno-fmaciel/mental-health-dashboard)
        - README: [README.md](https://github.com/Bruno-fmaciel/mental-health-dashboard/blob/main/README.md)
        """)
    
    with col2:
        st.markdown("""
        **Artefatos:**
        
        - Dashboard Online: *Adicionar link do Streamlit Cloud*
        - Google Site: [GTI 2025-2 Projetos 5 - Grupo 6](https://sites.google.com/cesar.school/gti-2025-2-projetos-5-grupo-6/in%C3%ADcio)
        """)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# REFERENCES
# ====================================
with st.container():
    st.subheader("📖 Referências Bibliográficas")
    
    st.markdown("""
    - Davenport, T. (2022). *Workforce Well-being and Burnout Research.*
    - WHO – World Health Organization. *Burn-out an "occupational phenomenon".*
    - Few, S. (2013). *Information Dashboard Design.*
    - Cole Nussbaumer Knaflic. (2015). *Storytelling with Data.*
    - Disciplina Projeto 5 — Material de Aula (CESAR School – GTI)
    """)

# ====================================
# FOOTER
# ====================================
st.markdown("<br><hr><center style='color:gray'>Dashboard • Projetos 5 — GTI • 2025</center>",
            unsafe_allow_html=True)
