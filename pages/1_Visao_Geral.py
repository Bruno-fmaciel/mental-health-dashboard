import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.charts import kpi_cards, dist_stress
from ui.insight_box import insight_box
from insights.overview import insights_overview

st.set_page_config(page_title="Visão Geral — SR2", page_icon="📊", layout="wide")

# ====================================
# TÍTULO E INTRODUÇÃO
# ====================================
st.title("📊 Visão Geral")

st.markdown("""
### 🎯 Objetivo do Dashboard

Este dashboard analisa **saúde mental e burnout no ambiente de trabalho**, com foco em:
- **Identificar segmentos de risco** (departamentos, cargos, modalidades)
- **Comparar impacto** de políticas organizacionais e condições de trabalho
- **Avaliar diferenças** entre trabalho remoto, híbrido e presencial

Use os **filtros na sidebar** para explorar diferentes perfis e responder perguntas como:
*"Desenvolvedores remotos com >50h/semana têm mais burnout?"*
""")

st.divider()

# ====================================
# CARREGA E FILTRA DADOS
# ====================================
df = load_data()
df_filtered = render_sidebar(df)

# Verifica se há dados
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Ajuste os filtros na sidebar.")
    st.stop()

# ====================================
# KPIs PRINCIPAIS
# ====================================
st.subheader("📈 Indicadores-Chave")
st.caption("Métricas principais do grupo atualmente selecionado. Use os filtros na sidebar para segmentar.")

kpi_cards(df_filtered)

st.divider()

# ====================================
# GRÁFICO DE DISTRIBUIÇÃO
# ====================================
st.subheader("📊 Distribuição de Estresse")
st.caption("Como o estresse está distribuído no grupo selecionado. Valores mais altos (>6) indicam maior risco.")

st.plotly_chart(dist_stress(df_filtered), use_container_width=True, key="dist_stress_visao_geral")

st.divider()

# ====================================
# CONTEXTO DOS DADOS
# ====================================
st.subheader("💡 Sobre os Dados")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Origem dos Dados**:
    - `dataset_principal.csv` - Saúde mental geral, hábitos e suporte psicológico
    - `dataset_burnout.csv` - Burnout, horas de trabalho e políticas organizacionais
    - `dataset_workplace.csv` - Trabalho remoto, produtividade e equilíbrio vida-trabalho
    
    Os três datasets foram **normalizados e unificados** para análise integrada.
    """)

with col2:
    st.markdown("""
    **Como Navegar**:
    1. 🏢 **Ambiente de Trabalho** - Compare políticas de suporte
    2. 🏠 **Remoto & Híbrido** - Analise diferenças entre modalidades
    3. 🧩 **Perfis & Segmentos** - Identifique grupos de alto risco
    4. 📊 Use os **filtros** para análises específicas
    """)

insights = insights_overview(df_filtered)

# Formata insights como lista HTML
formatted_items = "".join([f"<li>{i}</li>" for i in insights])
formatted = f"<ul style='margin-left: 20px;'>{formatted_items}</ul>"

# Renderiza usando o card estilizado
insight_box(
    title="🔍 Insights Automáticos da Visão Geral",
    content=formatted
)


# ====================================
# FOOTER
# ====================================
st.divider()
st.caption("💡 **Próximos passos**: Navegue pelas páginas no menu lateral para análises mais detalhadas.")
