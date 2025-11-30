import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.charts import small_multiples_segments
from ui.insight_box import insight_box
from insights.segments import insights_segments


st.set_page_config(page_title="Perfis & Segmentos — SR2", page_icon="🧩", layout="wide")

# ====================================
# TÍTULO E INTRODUÇÃO
# ====================================
st.title("🧩 Perfis & Segmentos")

# ====================================
# CARREGA E FILTRA DADOS
# ====================================
df = load_data()

# Aplica filtros (com filtro de segmentos ativado)
df_filtered = render_sidebar(df, show_segment_filter=True)

# Verifica se há dados após filtros
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Ajuste os filtros na sidebar.")
    st.stop()

# Mostra informações sobre os segmentos disponíveis
if 'segment' in df_filtered.columns:
    segments_list = df_filtered['segment'].dropna().unique()
    st.caption(f"📊 Analisando {len(segments_list)} segmentos: {', '.join(segments_list)}")
else:
    st.warning("Coluna 'segment' não encontrada nos dados. Verifique o mapeamento em `utils/data_io.py`.")
    st.stop()

# ====================================
# GRÁFICO PRINCIPAL: PERFIL DE RISCO
# ====================================

#st.caption("Compare métricas-chave entre diferentes segmentos. Segmentos com alto estresse e alta % de burnout apresentam perfil crítico neste conjunto de dados.")

st.plotly_chart(small_multiples_segments(df_filtered), use_container_width=True, key="small_multiples_segments")

# ====================================
# RANKING DE SEGMENTOS CRÍTICOS
# ====================================
st.subheader("⚠️ Segmentos de Maior Risco")

# Calcula score de risco
if 'burnout_level' in df_filtered.columns:
    risk_by_segment = df_filtered.groupby('segment').agg({
        'stress_score': 'mean',
        'hours_per_week': 'mean',
        'segment': 'count'
    }).rename(columns={'segment': 'n_total'})
    
    # Calcula % burnout alto
    burnout_high = df_filtered[df_filtered['burnout_level'] == 'high'].groupby('segment').size()
    risk_by_segment['pct_burnout_high'] = (burnout_high / risk_by_segment['n_total'] * 100).fillna(0).round(1)
    
    # Ordena por % burnout alto (decrescente)
    risk_by_segment = risk_by_segment.sort_values('pct_burnout_high', ascending=False).reset_index()
    
    # Destaca TOP 3 críticos
    top3 = risk_by_segment.head(3)
    
    if len(top3) > 0:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for idx, row in enumerate(top3.itertuples()):
            if idx < len(cols):
                with cols[idx]:
                    st.metric(
                        f"#{idx+1} {row.segment}",
                        f"{row.pct_burnout_high:.1f}%",
                        delta=f"Estresse: {row.stress_score:.1f}",
                        delta_color="inverse",
                        help=f"{int(row.n_total)} respondentes • {row.hours_per_week:.0f}h/sem"
                    )
    else:
        st.info("Não há dados suficientes para calcular o ranking de segmentos críticos.")
else:
    st.info("Coluna 'burnout_level' não disponível. Ranking de risco não pode ser calculado.")

# ====================================
# TABELA DETALHADA - TODOS OS SEGMENTOS
# ====================================
st.divider()
st.subheader("📈 Estatísticas Detalhadas por Segmento")

st.caption("""
**Como usar esta tabela**: Procure segmentos com **alto estresse médio** (>6) **E** **alta % burnout alto** (>40%). 
Esses são os perfis que apresentam maior risco neste conjunto de dados e podem requerer atenção prioritária.
""")

if 'segment' in df_filtered.columns:
    # Cria tabela de estatísticas por segmento
    stats = df_filtered.groupby('segment').agg({
        'stress_score': ['mean', 'std', 'count'],
        'hours_per_week': 'mean'
    }).round(2)
    
    stats.columns = ['Estresse (Média)', 'Estresse (Desvio)', 'N° Respondentes', 'Horas/Sem (Média)']
    
    # Adiciona % burnout se disponível
    if 'burnout_level' in df_filtered.columns:
        burnout_stats = df_filtered[df_filtered['burnout_level'] == 'high'].groupby('segment').size()
        total_by_segment = df_filtered.groupby('segment').size()
        stats['% Burnout Alto'] = (burnout_stats / total_by_segment * 100).round(1)
        
        # ORDENA por % Burnout Alto (decrescente) para destacar críticos
        stats = stats.sort_values('% Burnout Alto', ascending=False)
    
    # Aplica gradiente de cores para destacar valores críticos
    styled_df = stats.style.background_gradient(
        subset=['Estresse (Média)'],
        cmap='Reds',
        vmin=0,
        vmax=10
    )
    
    # Adiciona gradiente para % Burnout Alto se a coluna existir
    if '% Burnout Alto' in stats.columns:
        styled_df = styled_df.background_gradient(
            subset=['% Burnout Alto'],
            cmap='OrRd',
            vmin=0,
            vmax=100
        )
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400
    )

# KPI geral para benchmark
st.markdown("#### 📊 Benchmarks Gerais (para comparação)")

col1, col2, col3 = st.columns(3)

with col1:
    if 'stress_score' in df_filtered.columns:
        avg_stress = df_filtered['stress_score'].mean()
        st.metric("Estresse Médio Geral", f"{avg_stress:.1f}")

with col2:
    if 'burnout_level' in df_filtered.columns:
        pct_high_general = (df_filtered['burnout_level'] == 'high').mean() * 100
        st.metric("% Burnout Alto Geral", f"{pct_high_general:.1f}%")

with col3:
    if 'hours_per_week' in df_filtered.columns:
        avg_hours = df_filtered['hours_per_week'].mean()
        st.metric("Horas/Sem Média Geral", f"{avg_hours:.1f}h")

# ====================================
# INSIGHTS
# ====================================
insight_box("🔥 Insights Automáticos de Burnout", insights_segments(df_filtered))

# ====================================
# FOOTER
# ====================================
st.caption("💡 Combine esta análise de segmentos com os filtros de cargo e modalidade para identificar perfis de risco ainda mais específicos.")
