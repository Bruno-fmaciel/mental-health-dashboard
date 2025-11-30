import streamlit as st
import pandas as pd
from utils.data_io import load_data

st.set_page_config(
    page_title="Sobre & Métodos — SR2",
    page_icon="ℹ️",
    layout="wide"
)

# ======================================================
# HEADER — IDENTIDADE VISUAL
# ======================================================
st.markdown("""
<div style="
    padding: 22px; 
    border-radius: 12px;
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    margin-bottom: 25px;
">
    <h1 style="margin:0; color:#93c5fd;">ℹ️ Sobre & Métodos</h1>
    <p style="margin:0; color:#e2e8f0; font-size:15px;">
        Documentação oficial do dashboard — metodologia, dados, decisões analíticas e referências do projeto.
    </p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# RESUMO AUTOMÁTICO
# ======================================================
st.subheader("📝 Resumo da Base de Dados Utilizada")

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
### 📌 Panorama Geral dos Dados

- Total de respondentes integrados: **{total}**
- Estresse médio geral: **{stress_mean:.2f}**
- Horas semanais médias: **{hours_mean:.1f}h**
- % de burnout alto: **{pct_high:.1f}%**  
  """)

# ======================================================
# PROBLEMA / QUESTÕES
# ======================================================
st.markdown("""
---
### 🎯 Problema e Perguntas de Pesquisa

**Problema central**  
Organizações enfrentam aumento de estresse e burnout no trabalho, mas carecem de visão integrada sobre *quem são os grupos de risco* e *quais fatores organizacionais mais influenciam esse cenário*.

**Perguntas que guiamos no projeto:**
1. Quais segmentos apresentam maior risco de burnout?
2. A carga horária semanal influencia diretamente o estresse?
3. Modalidade de trabalho (remoto/híbrido/presencial) impacta o bem-estar?
4. Políticas organizacionais estão associadas a menor risco?
5. Como diferentes dimensões (cargo, horas, departamento, política) interagem?

---
""")

# ======================================================
# DADOS E PREPARAÇÃO
# ======================================================
st.markdown("""
### 📊 Dados & Preparação

**Fontes integradas no projeto:**
- `dataset_principal.csv` — saúde mental, hábitos e características individuais  
- `dataset_burnout.csv` — níveis de estresse e burnout  
- `dataset_workplace.csv` — modalidades de trabalho, satisfação, políticas  

**Principais etapas de preparação:**
- Normalização de `work_mode` → remoto / híbrido / presencial  
- Padronização de cargos e segmentos  
- Conversão de estresse para escala 0–10  
- Criação da variável categórica `burnout_level`  
- Unificação dos 3 datasets com chaves compatíveis  
- Remoção de entradas inválidas e excesso de nulos  

**Limitações da base:**
- Dados auto-reportados → viés de percepção  
- Diferenças de estrutura entre datasets  
- Amostras pequenas em alguns segmentos  
- Não há dados longitudinais (não medimos mudança no tempo)  
---
""")

# ======================================================
# METODOLOGIAS
# ======================================================
st.markdown("""
### 🔬 Metodologias Utilizadas

#### ✔ CRISP-DM (Adaptado)
1. Entendimento do negócio  
2. Entendimento dos dados  
3. Preparação da base integrada  
4. Modelagem visual (dashboards e KPIs)  
5. Avaliação de hipóteses  
6. Deploy (Streamlit Cloud)

#### ✔ Storytelling com Dados
- Títulos que comunicam a “mensagem” do gráfico  
- Comparações diretas entre grupos  
- Destaque a riscos e tendências  
- Priorização de KPIs no topo

#### ✔ Boas práticas de design de dashboards
- Layout horizontal (wide)  
- Gráficos interativos com Plotly  
- Uso consistente de cores  
- Cartões de KPI  
- Insights automáticos por página  

---
""")

# ======================================================
# TIME / LINKS
# ======================================================
st.markdown("### 👥 Time & Artefatos do Projeto")

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
- GitHub: https://github.com/Bruno-fmaciel/mental-health-dashboard
- README do projeto:https://github.com/Bruno-fmaciel/mental-health-dashboard/blob/main/README.md
""")

with col2:
    st.markdown("""
**Artefatos:**
- Dashboard Online: *Adicionar link do Streamlit Cloud*
- Google Site: https://sites.google.com/cesar.school/gti-2025-2-projetos-5-grupo-6/in%C3%ADcio
- Slides da Apresentação: *(Adicionar link aqui)*
""")

# ======================================================
# REFERÊNCIAS
# ======================================================
st.markdown("""
---
### 📖 Referências Bibliográficas

- Davenport, T. (2022). *Workforce Well-being and Burnout Research.*  
- WHO – World Health Organization. *Burn-out an "occupational phenomenon".*  
- Few, S. (2013). *Information Dashboard Design.*  
- Cole Nussbaumer Knaflic. (2015). *Storytelling with Data.*  
- Projeto SR2 — Material de Aula (CESAR School – GTI)

---
""")
