import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.charts import stacked_env_policies, compare_policies_risk
from ui.insight_box import insight_box
from insights.enviroments import insights_enviroments


st.set_page_config(page_title="Ambiente de Trabalho — SR2", page_icon="🏢", layout="wide")

# ====================================
# TÍTULO E INTRODUÇÃO
# ====================================
st.title("🏢 Ambiente de Trabalho e Políticas Organizacionais")

st.markdown("""
<div style='background-color: rgba(42, 42, 42, 0.3); padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #2980b9; margin-bottom: 2rem;'>

### 🎯 Perguntas-chave desta análise

- **Quais políticas de suporte** estão associadas a menor risco de burnout?
- **Ter acesso a recursos de saúde mental** faz diferença mensurável no bem-estar?
- **Como diferentes condições organizacionais** impactam o estresse e o esgotamento dos colaboradores?

Esta página explora como as **políticas e condições do ambiente de trabalho** influenciam 
o risco de burnout, complementando a análise de modalidades (Remoto/Híbrido) e características individuais.

</div>
""", unsafe_allow_html=True)

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
# SELEÇÃO DE DIMENSÃO DE POLÍTICA
# ====================================
st.divider()
st.subheader("📊 Análise de Políticas")

# Identifica dimensões disponíveis
available_dimensions = []
dimension_labels = {
    'policy': '🛡️ Políticas de Suporte à Saúde Mental',
    'work_mode': '💼 Modalidade de Trabalho (já analisada em outra página)',
    'segment': '🏭 Segmentos/Departamentos'
}

for col in ['policy', 'segment']:
    if col in df_filtered.columns and df_filtered[col].notna().sum() > 0:
        available_dimensions.append(col)

if not available_dimensions:
    st.error("❌ Nenhuma dimensão de política disponível nos dados filtrados.")
    st.stop()

# Selectbox para escolher dimensão (se houver múltiplas)
if len(available_dimensions) > 1:
    selected_dimension = st.selectbox(
        "Selecione a dimensão para análise:",
        options=available_dimensions,
        format_func=lambda x: dimension_labels.get(x, x),
        help="Escolha qual aspecto organizacional você quer analisar em relação ao burnout"
    )
else:
    selected_dimension = available_dimensions[0]
    st.caption(f"Analisando: **{dimension_labels.get(selected_dimension, selected_dimension)}**")

# ====================================
# KPIs RÁPIDOS
# ====================================
st.markdown("### 📈 Indicadores-Chave")

# Calcula estatísticas de risco por política
risk_stats = compare_policies_risk(df_filtered, policy_col=selected_dimension)

if risk_stats.empty:
    st.warning("⚠️ Não há dados suficientes para análise de políticas.")
    st.stop()

# KPIs em colunas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Políticas Analisadas",
        len(risk_stats),
        help=f"Número de categorias distintas em {selected_dimension}"
    )

with col2:
    top_risk = risk_stats.iloc[0]
    st.metric(
        "⚠️ Maior Risco",
        f"{top_risk['pct_high']:.1f}%",
        delta=f"{top_risk[selected_dimension]}",
        delta_color="inverse",
        help="Política/condição com maior % de burnout alto"
    )

with col3:
    low_risk = risk_stats.iloc[-1]
    st.metric(
        "✅ Menor Risco",
        f"{low_risk['pct_high']:.1f}%",
        delta=f"{low_risk[selected_dimension]}",
        delta_color="normal",
        help="Política/condição com menor % de burnout alto"
    )

with col4:
    avg_high = risk_stats['pct_high'].mean()
    st.metric(
        "Média de Alto Risco",
        f"{avg_high:.1f}%",
        help="Percentual médio de burnout alto entre todas as políticas"
    )

# ====================================
# GRÁFICO PRINCIPAL: STACKED BAR
# ====================================
st.divider()
st.subheader("📊 Distribuição de Burnout por Política")

st.caption("""
O gráfico abaixo mostra a **proporção** de colaboradores em cada nível de burnout (baixo, médio, alto) 
para cada política/condição. Cada barra soma 100%, permitindo comparar a composição de risco entre políticas.
""")

fig = stacked_env_policies(df_filtered, policy_col=selected_dimension, min_pct=5.0, show_percentages=True)
st.plotly_chart(fig, use_container_width=True, key="stacked_env_chart")

# ====================================
# TABELA DETALHADA
# ====================================
st.divider()
st.subheader("📋 Detalhamento por Política")

st.caption("Tabela com estatísticas detalhadas de cada política/condição, ordenada por risco (maior → menor).")

# Formata tabela para exibição
display_df = risk_stats.copy()
display_df.columns = [
    'Política/Condição', 
    'Total (N)', 
    '% Alto Risco', 
    '% Risco Médio', 
    '% Baixo Risco'
]

# Aplica estilo com gradiente de cores
st.dataframe(
    display_df.style.background_gradient(
        subset=['% Alto Risco'],
        cmap='Reds',
        vmin=0,
        vmax=100
    ).background_gradient(
        subset=['% Baixo Risco'],
        cmap='Greens',
        vmin=0,
        vmax=100
    ).format({
        '% Alto Risco': '{:.1f}%',
        '% Risco Médio': '{:.1f}%',
        '% Baixo Risco': '{:.1f}%'
    }),
    use_container_width=True,
    height=400
)

# Botão de download
csv = risk_stats.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar Dados (CSV)",
    data=csv,
    file_name=f"analise_politicas_{selected_dimension}.csv",
    mime="text/csv",
    help="Exporta a tabela completa para análise externa"
)

# ====================================
# NOTAS DE INTERPRETAÇÃO
# ====================================
st.divider()
st.markdown("### 💡 Como Interpretar os Resultados")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 📖 Lendo o Gráfico
    
    - **Barras vermelhas (alto risco)**: Indicam % de colaboradores com burnout alto
    - **Políticas com mais vermelho**: Grupos mais críticos que precisam de atenção
    - **Políticas com mais verde**: Condições associadas a menor risco
    - **Comparação horizontal**: Permite identificar qual política é mais protetora
    
    ⚠️ **Atenção**: Categorias com menos de 5% dos dados são agrupadas em "Outros".
    """)

with col2:
    st.markdown("""
    #### 🎯 Próximos Passos
    
    1. **Identifique políticas críticas**: Foque nas com >50% de alto risco
    2. **Compare com benchmark**: A média geral está em {:.1f}%
    3. **Investigue causas**: Por que certas políticas têm mais/menos risco?
    4. **Ações recomendadas**:
       - Expandir políticas protetoras (menor risco)
       - Reforçar suporte em políticas críticas
       - Considerar pilotos de intervenção
    
    💬 **Combine com outros filtros** na sidebar para análises mais específicas!
    """.format(avg_high))

# ====================================
# INSIGHTS CONTEXTUAIS
# ====================================
st.divider()
st.markdown("### 🔍 Insights Contextuais")

# Identifica política mais/menos protetora
best_policy = risk_stats.iloc[-1]
worst_policy = risk_stats.iloc[0]
delta = worst_policy['pct_high'] - best_policy['pct_high']

st.info(f"""
**Diferença de impacto**: Colaboradores em **"{worst_policy[selected_dimension]}"** têm **{delta:.1f} pontos 
percentuais a mais** de risco alto comparado a **"{best_policy[selected_dimension]}"**.

Isso sugere que a política/condição organizacional tem **impacto significativo** no bem-estar 
e deve ser considerada em estratégias de prevenção de burnout.
""")

# Aviso sobre tamanho de amostra
min_n = risk_stats['n_total'].min()
if min_n < 30:
    st.warning(f"""
    ⚠️ **Atenção à amostra**: Algumas políticas têm poucos respondentes (mínimo: {min_n}). 
    Resultados com amostras pequenas devem ser interpretados com cautela.
    """)

# ====================================
# INSIGHTS
# ====================================
insight_box("🔥 Insights Automáticos de Burnout", insights_enviroments(df_filtered))

# ====================================
# FOOTER
# ====================================
st.divider()
st.caption("💡 **Dica**: Use os filtros na sidebar para segmentar a análise por cargo, modalidade ou carga horária.")
