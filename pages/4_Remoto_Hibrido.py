import streamlit as st
import pandas as pd
from utils.data_io import load_data, render_sidebar
from utils.charts import (
    violin_by_workmode,
    compute_risk_delta_by_mode_segment,
    plot_risk_bars_remote_hybrid,
    plot_delta_lollipop,
    plot_delta_heatmap
)

st.set_page_config(page_title="Remoto & Híbrido — SR2", page_icon="🏠", layout="wide")

st.title("🏠 Remoto & Híbrido")

# Carrega dados
df = load_data()
df = render_sidebar(df)

# Verifica se há dados
if df.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados.")
    st.stop()

# Tabs para organizar as análises
tab1, tab2 = st.tabs(["📊 Análise de Deltas", "🎻 Distribuições"])

# ============== TAB 1: Análise de Deltas Remote vs Hybrid ==============
with tab1:
    st.header("Remoto vs Híbrido — Análise de Risco e Deltas")
    
    st.markdown("""
    Esta análise compara o risco de burnout/estresse entre trabalho **Remoto** e **Híbrido**.
    
    **Delta (Δ)** = % Risco Remoto - % Risco Híbrido
    - **Positivo**: Remoto tem mais risco
    - **Negativo**: Híbrido tem mais risco
    """)
    
    # —— Sidebar de configuração ——
    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Configurações de Análise")
    
    # Detecta colunas disponíveis
    available_segments = []
    segment_options = {
        'gender': 'Gênero',
        'age_group': 'Faixa Etária',
        'Region': 'Região',
        'Industry': 'Indústria',
        'segment': 'Segmento (Depto/Região)',
        'Department': 'Departamento'
    }
    
    for col, label in segment_options.items():
        if col in df.columns and df[col].notna().any():
            available_segments.append((col, label))
    
    if not available_segments:
        st.error("❌ Nenhuma coluna de segmento disponível nos dados filtrados.")
        st.stop()
    
    segmento = st.sidebar.selectbox(
        "Segmento primário",
        options=[s[0] for s in available_segments],
        format_func=lambda x: dict(available_segments).get(x, x),
        index=0,
        help="Dimensão pela qual você quer comparar Remote vs Hybrid"
    )
    
    metrica = st.sidebar.selectbox(
        "Métrica de risco",
        options=["burnout_high", "stress_threshold"],
        format_func=lambda x: "🔥 Burnout Alto" if x == "burnout_high" else "😰 Estresse ≥ Limiar",
        index=0,
        help="Qual indicador usar para calcular o risco"
    )
    
    limiar = st.sidebar.slider(
        "Limiar de stress (se aplicável)", 
        5.0, 9.0, 7.0, 0.5,
        help="Usado apenas se métrica = 'Estresse ≥ Limiar'"
    )
    
    min_n = st.sidebar.number_input(
        "Amostra mínima por grupo", 
        5, 200, 15, 5,
        help="Filtra grupos com poucos respondentes para evitar conclusões frágeis"
    )
    
    # —— Cálculo ——
    try:
        delta_df = compute_risk_delta_by_mode_segment(
            df, segment_col=segmento, risk_metric=metrica,
            stress_threshold=limiar, min_n=min_n
        )
        
        if delta_df.empty:
            st.warning(f"⚠️ Nenhum grupo com amostra ≥ {min_n}. Reduza o mínimo ou ajuste os filtros.")
            st.stop()
        
        # Ordena pelo maior |delta| (absoluto)
        delta_df['abs_delta'] = delta_df['delta_pct'].abs()
        delta_df = delta_df.sort_values('abs_delta', ascending=False)
        
    except Exception as e:
        st.error(f"❌ Erro ao calcular deltas: {str(e)}")
        st.stop()
    
    # —— KPIs ——
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Grupos Analisados",
            len(delta_df),
            help=f"Grupos com n ≥ {min_n}"
        )
    
    with col2:
        top_delta = delta_df.iloc[0]
        st.metric(
            "Maior |Δ|",
            f"{top_delta['abs_delta']:.1f}pp",
            help=f"{top_delta[segmento]}: {top_delta['delta_pct']:+.1f}pp"
        )
    
    with col3:
        avg_remote = delta_df['risk_Remote_pct'].mean()
        avg_hybrid = delta_df['risk_Hybrid_pct'].mean()
        st.metric(
            "Risco Médio",
            f"R: {avg_remote:.1f}% | H: {avg_hybrid:.1f}%",
            delta=f"{avg_remote - avg_hybrid:+.1f}pp"
        )
    
    # —— Gráfico 1: Barras comparativas ——
    st.subheader("📊 Risco por Modalidade (Remote x Hybrid)")
    st.caption("Exibe % de alto risco em cada modalidade para cada valor do segmento selecionado.")
    st.plotly_chart(
        plot_risk_bars_remote_hybrid(delta_df, segmento), 
        use_container_width=True,
        key="risk_bars"
    )
    
    # —— Gráfico 2: Lollipop de deltas ——
    st.subheader("🎯 Delta de Risco por Segmento")
    st.caption("Δ (pontos percentuais) = Remoto − Híbrido. Positivo indica risco maior em Remote.")
    
    # Destaca top-3
    top3 = delta_df.nlargest(3, 'abs_delta')[segmento].tolist()
    st.info(f"**Top 3 maiores |Δ|**: {', '.join(map(str, top3))}")
    
    st.plotly_chart(
        plot_delta_lollipop(delta_df, segmento), 
        use_container_width=True,
        key="delta_lollipop"
    )
    
    # —— Tabela detalhada ——
    st.subheader("📋 Dados Detalhados")
    
    # Prepara tabela para exibição
    display_df = delta_df[[
        segmento, 
        'risk_Remote_pct', 'n_Remote',
        'risk_Hybrid_pct', 'n_Hybrid',
        'delta_pct'
    ]].copy()
    
    display_df.columns = [
        segmento,
        'Remoto (%)', 'n Remoto',
        'Híbrido (%)', 'n Híbrido',
        'Δ (pp)'
    ]
    
    # Destaca deltas maiores
    st.dataframe(
        display_df.style.background_gradient(
            subset=['Δ (pp)'],
            cmap='RdYlGn_r',  # Vermelho = positivo (remoto pior)
            vmin=-20, vmax=20
        ),
        use_container_width=True
    )
    
    # —— Download CSV ——
    csv = delta_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados (CSV)",
        data=csv,
        file_name=f"delta_remote_hybrid_{segmento}.csv",
        mime="text/csv",
        help="Exporta a tabela completa com todos os cálculos"
    )
    
    # —— Heatmap opcional (2 dimensões) ——
    with st.expander("🔥 Heatmap Avançado — Comparar 2 Segmentos"):
        st.caption("Útil para ver interações entre duas dimensões (ex: Gênero × Região)")
        
        col1, col2 = st.columns(2)
        
        available_for_heatmap = [s[0] for s in available_segments]
        
        with col1:
            r = st.selectbox(
                "Linhas (segmento A)", 
                available_for_heatmap,
                format_func=lambda x: dict(available_segments).get(x, x),
                key="heatmap_rows"
            )
        
        with col2:
            c = st.selectbox(
                "Colunas (segmento B)", 
                [x for x in available_for_heatmap if x != r],
                format_func=lambda x: dict(available_segments).get(x, x),
                key="heatmap_cols"
            )
        
        try:
            st.plotly_chart(
                plot_delta_heatmap(
                    df, rows_col=r, cols_col=c, 
                    risk_metric=metrica, stress_threshold=limiar
                ),
                use_container_width=True,
                key="delta_heatmap"
            )
        except Exception as e:
            st.warning(f"⚠️ Não foi possível gerar o heatmap: {str(e)}")

# ============== TAB 2: Distribuições (análise original) ==============
with tab2:
    st.header("Distribuições por Modalidade de Trabalho")
    st.caption("Visualização completa de como o estresse se distribui em cada modalidade")
    
    st.plotly_chart(
        violin_by_workmode(df), 
        use_container_width=True, 
        key="violin_by_workmode"
    )
    
    # Estatísticas complementares
    if 'work_mode' in df.columns and 'stress_score' in df.columns:
        st.subheader("📈 Estatísticas por Modalidade")
        
        stats = df.groupby('work_mode')['stress_score'].agg([
            ('Média', 'mean'),
            ('Mediana', 'median'),
            ('Desvio Padrão', 'std'),
            ('Mínimo', 'min'),
            ('Máximo', 'max'),
            ('N', 'count')
        ]).round(2)
        
        st.dataframe(stats, use_container_width=True)

# —— Footer ——
st.divider()
st.markdown("""
### 💡 Como Interpretar os Resultados

**Delta positivo (+)**: 
- Trabalho remoto apresenta maior risco que híbrido neste segmento
- Pode indicar: isolamento social, falta de suporte, dificuldade de desconexão

**Delta negativo (−)**:
- Trabalho híbrido apresenta maior risco que remoto
- Pode indicar: estresse de transição, sobrecarga com deslocamento

**Delta próximo de zero**:
- Risco similar entre modalidades neste segmento
- A modalidade pode não ser o fator determinante

**Amostra mínima**: 
- Grupos com poucos respondentes (< {}) foram filtrados para evitar conclusões frágeis
- Ajuste o parâmetro na sidebar se necessário
""".format(min_n))
