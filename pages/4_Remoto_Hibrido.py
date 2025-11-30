import streamlit as st
from utils.data_io import load_data, render_sidebar
import plotly.express as px
from ui.insight_box import insight_box
from insights.modalidades import insights_modalidades
from utils.charts import plot_delta_heatmap


st.set_page_config(layout="wide", page_title="Modalidades de Trabalho")

df = load_data()
filtered = render_sidebar(df)

# Validação de DataFrame vazio
if filtered.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

st.title("🏠 Modalidades de Trabalho")

# ============================
# KPIs por modalidade
# ============================
st.caption("Compare os padrões de estresse e carga horária entre diferentes modalidades de trabalho neste conjunto de dados.")

group_cols = ["stress_score", "hours_per_week"]

if "work_mode" not in filtered.columns:
    st.error("A coluna 'work_mode' não existe no dataframe final. Verifique load_data().")
    st.stop()

modalidade_stats = (
    filtered
    .groupby("work_mode")[group_cols]
    .mean()
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    st.caption("Estresse médio por modalidade. Observe os padrões e diferenças entre remoto, híbrido e presencial.")
    fig = px.bar(
        modalidade_stats,
        x="work_mode",
        y="stress_score",
        title="Estresse Médio por Modalidade",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.caption("Horas semanais médias por modalidade. Compare a carga de trabalho entre diferentes modalidades.")
    fig = px.bar(
        modalidade_stats,
        x="work_mode",
        y="hours_per_week",
        title="Horas Semanais Médias por Modalidade",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ============================
# Distribuição de Estresse
# ============================
st.subheader("📈 Distribuição de Estresse por Modalidade")
st.caption("Distribuição detalhada do estresse em cada modalidade. Observe a variabilidade e possíveis diferenças entre grupos.")

fig = px.box(
    filtered,
    x="work_mode",
    y="stress_score",
    title="Distribuição de Estresse"
)
st.plotly_chart(fig, use_container_width=True)

# ====================================
# ANÁLISE AVANÇADA - HEATMAP EXPLORATÓRIO
# ====================================
with st.expander("🔬 Análise Avançada: Heatmap de Delta Remoto × Híbrido", expanded=False):
    st.markdown("""
    **O que você está vendo:**
    
    Este heatmap mostra a **diferença de risco** entre trabalho remoto e híbrido (Δ = Remoto - Híbrido) 
    em pontos percentuais, cruzando duas dimensões de segmentação.
    
    - **Valores positivos (vermelho)**: Remoto tem maior risco que Híbrido neste grupo
    - **Valores negativos (azul)**: Híbrido tem maior risco que Remoto neste grupo
    - **Valores próximos de zero**: Risco similar entre as modalidades
    
    ⚠️ **Atenção**: Combinações com poucos respondentes devem ser interpretadas com cuidado.
    """)
    
    # Identifica colunas categóricas disponíveis
    categorical_cols = []
    potential_cols = ['role', 'segment', 'gender', 'age_group', 'policy']
    
    for col in potential_cols:
        if col in filtered.columns and filtered[col].notna().sum() > 10:
            unique_vals = filtered[col].dropna().nunique()
            if unique_vals >= 2:  # Precisa ter pelo menos 2 valores únicos
                categorical_cols.append(col)
    
    if len(categorical_cols) < 2:
        st.warning("⚠️ Não há colunas categóricas suficientes com dados para gerar o heatmap. "
                  "Necessário pelo menos 2 colunas com dados válidos.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            rows_col = st.selectbox(
                "Selecione a dimensão para as linhas:",
                options=categorical_cols,
                help="Esta dimensão aparecerá nas linhas do heatmap"
            )
        
        with col2:
            # Remove a coluna selecionada para linhas das opções de colunas
            cols_options = [c for c in categorical_cols if c != rows_col]
            if not cols_options:
                st.warning("⚠️ Não há outra dimensão disponível para as colunas.")
                cols_col = None
            else:
                cols_col = st.selectbox(
                    "Selecione a dimensão para as colunas:",
                    options=cols_options,
                    help="Esta dimensão aparecerá nas colunas do heatmap"
                )
        
        if cols_col:
            # Prepara DataFrame temporário com valores capitalizados para work_mode
            # (a função plot_delta_heatmap espera "Remote" e "Hybrid" com primeira letra maiúscula)
            df_heatmap = filtered.copy()
            
            # Capitaliza work_mode temporariamente para a função
            if 'work_mode' in df_heatmap.columns:
                df_heatmap['work_mode'] = df_heatmap['work_mode'].str.capitalize()
                # Mapeia valores específicos
                df_heatmap['work_mode'] = df_heatmap['work_mode'].replace({
                    'Remote': 'Remote',
                    'Hybrid': 'Hybrid',
                    'Onsite': 'Onsite'  # Presencial não será usado, mas mantém consistência
                })
            
            # Verifica se há dados de Remote e Hybrid
            has_remote_hybrid = df_heatmap['work_mode'].isin(['Remote', 'Hybrid']).any()
            
            if not has_remote_hybrid:
                st.info("ℹ️ Este heatmap compara apenas trabalho Remoto e Híbrido. "
                       "Não há dados suficientes dessas modalidades nos filtros selecionados.")
            else:
                try:
                    fig_heatmap = plot_delta_heatmap(
                        df_heatmap,
                        rows_col=rows_col,
                        cols_col=cols_col,
                        mode_col="work_mode"
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                    
                    st.caption("""
                    💡 **Como interpretar**: 
                    - Valores positivos indicam que Remoto apresenta maior risco que Híbrido naquela combinação
                    - Valores negativos indicam que Híbrido apresenta maior risco que Remoto
                    - Células vazias ou com poucos dados podem não aparecer (filtro de amostra mínima)
                    """)
                except Exception as e:
                    st.error(f"❌ Erro ao gerar heatmap: {str(e)}")
                    st.caption("Verifique se há dados suficientes para as dimensões selecionadas.")

# ====================================
# INSIGHTS
# ====================================
insight_box("🔥 Insights Automáticos de Burnout", insights_modalidades(filtered))

