import streamlit as st
import plotly.express as px
from utils.data_io import load_data, render_sidebar
from utils.charts import scatter_hours_burnout, box_burnout_by_role
from ui.insight_box import insight_box
from insights.burnout import insights_burnout

st.set_page_config(page_title="Burnout — SR2", page_icon="🔥", layout="wide")

# ====================================
# TÍTULO E INTRODUÇÃO
# ====================================
st.title("🔥 Burnout e Carga de Trabalho")

# with st.expander("Como pensamos esta análise?"):
#     st.markdown(
#         """
#         Nesta página não estamos provando causa e efeito, mas olhando para **padrões de associação**.
#         Em outras palavras: *neste conjunto de dados*, certos contextos de trabalho aparecem mais
#         frequentemente com estresse e burnout altos.

#         Isso ajuda a levantar hipóteses do tipo:
#         - “Equipes com comunicação mais clara parecem relatar menos burnout?”
#         - “Falta de apoio psicológico aparece junto com mais casos de burnout alto?”
#         """
#     )


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
st.caption("Distribuição do nível de estresse no grupo analisado (escala 0-10). Valores acima de 6 indicam alto estresse neste conjunto de dados.")

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
    st.caption("Relação entre horas trabalhadas por semana e nível de estresse. Observe se há associação positiva neste conjunto de dados.")
    st.plotly_chart(scatter_hours_burnout(df_filtered), use_container_width=True, key="scatter_hours_burnout")
with c2:
    st.markdown("#### 👥 Estresse por Cargo")
    st.caption("Distribuição de estresse entre diferentes ocupações. Compare os padrões e identifique cargos com maior variabilidade.")
    st.plotly_chart(box_burnout_by_role(df_filtered), use_container_width=True, key="box_burnout_by_role")

# ====================================
# INSIGHTS
# ====================================
insight_box("🔥 Insights Automáticos de Burnout", insights_burnout(df_filtered))

# ====================================
# FOOTER
# ====================================
st.caption("💡 Explore 'Ambiente de Trabalho' para ver como políticas de suporte impactam o burnout.")