import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_io import load_data, render_sidebar
from utils.charts import scatter_hours_burnout, box_burnout_by_role
from ui.insight_box import insight_box
from insights.burnout import insights_burnout

st.set_page_config(page_title="Burnout — SR2", page_icon="🔥", layout="wide")

# ====================================
# TÍTULO E INTRODUÇÃO
# ====================================
st.title("🔥 Deep Dive: Burnout e Intensidade de Trabalho")

st.markdown("""
<div style='background-color: rgba(42, 42, 42, 0.3); padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #FF6B6B; margin-bottom: 2rem;'>

### 🎯 Foco desta Análise

Esta página explora a **relação entre intensidade de trabalho e risco de burnout**:
- **Longas jornadas** aumentam o estresse?
- **Cargos específicos** são mais vulneráveis?
- **Há um ponto de virada** onde o risco dispara?

Use os **filtros na sidebar** para focar em grupos específicos (ex: só remotos, só híbridos, departamentos críticos).

</div>
""", unsafe_allow_html=True)

st.divider()

# ====================================
# CARREGA E FILTRA DADOS
# ====================================
# Carrega dados normalizados (todos os datasets)
df = load_data()

# Aplica filtros globais da sidebar
df_filtered = render_sidebar(df)

# Verifica se há dados após filtros
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Ajuste os filtros na sidebar.")
    st.stop()

# ====================================
# DISTRIBUIÇÃO DE ESTRESSE
# ====================================
st.subheader("📊 Distribuição do Estresse")
st.caption("Histograma do score de estresse (escala 0-10). Valores acima de 6 indicam alto estresse.")

# Usa coluna normalizada 'stress_score' (escala 0-10)
if 'stress_score' in df_filtered.columns:
    fig = px.histogram(
        df_filtered, 
        x='stress_score', 
        nbins=20,
        title="Distribuição do Estresse (Score 0-10)",
        labels={'stress_score': 'Score de Estresse'},
        color_discrete_sequence=['#FF6B6B']
    )
    fig.update_layout(
        xaxis_title="Score de Estresse (0-10)",
        yaxis_title="Número de Respondentes",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, key="hist_stress_burnout")
else:
    st.warning("⚠️ Coluna 'stress_score' não encontrada nos dados.")

st.divider()

# ====================================
# ANÁLISES COMPARATIVAS
# ====================================
st.subheader("🔍 Análises Comparativas")

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### ⏰ Horas de Trabalho × Estresse")
    st.caption("Quanto mais horas trabalhadas, maior o estresse?")
    st.plotly_chart(scatter_hours_burnout(df_filtered), use_container_width=True, key="scatter_hours_burnout")
with c2:
    st.markdown("#### 👥 Estresse por Cargo")
    st.caption("Compare a distribuição de estresse entre diferentes ocupações.")
    st.plotly_chart(box_burnout_by_role(df_filtered), use_container_width=True, key="box_burnout_by_role")

st.divider()

# ====================================
# INSIGHTS E PRÓXIMOS PASSOS
# ====================================
st.subheader("💡 Insights e Recomendações")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 📊 O que observar
    
    - **Correlação positiva** entre horas e estresse (quanto mais horas, mais estresse)
    - **Outliers**: pessoas com poucas horas mas alto estresse (outras causas?)
    - **Cargos com distribuição mais dispersa** (heterogeneidade na equipe)
    - **Pontos de virada**: há um limiar de horas onde o risco dispara?
    
    💡 Use os filtros para comparar grupos específicos (ex: Remote vs Hybrid).
    """)

with col2:
    st.markdown("""
    #### 🎯 Ações sugeridas
    
    - **Limitar jornadas** acima de 45h/semana
    - **Investigar cargos** com alto estresse médio
    - **Implementar políticas** de descanso obrigatório
    - **Monitorar continuamente** grupos de alto risco
    - **Considerar rotação** em funções de alta pressão
    
    ⚠️ Atenção especial a cargos com estresse consistentemente >7.
    """)

insights = insights_burnout(df_filtered)

formatted_items = "".join([f"<li>{i}</li>" for i in insights])
formatted = f"<ul style='margin-left: 20px;'>{formatted_items}</ul>"

insight_box(
    title="🔥 Insights Automáticos de Burnout",
    content=formatted
)

# ====================================
# FOOTER
# ====================================
st.divider()
st.caption("💡 **Próximos passos**: Explore 'Ambiente de Trabalho' para ver como políticas de suporte impactam o burnout.")