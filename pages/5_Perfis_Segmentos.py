import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.charts import small_multiples_segments

st.set_page_config(page_title="Perfis & Segmentos — SR2", page_icon="🧩", layout="wide")

st.title("🧩 Perfis & Segmentos")
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

# Gráfico principal de comparação
st.subheader("📊 Comparação de Métricas por Segmento")
st.plotly_chart(small_multiples_segments(df_filtered), use_container_width=True, key="small_multiples_segments")

# Informações adicionais
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("💡 Insights")
    st.markdown("""
    **Como interpretar**:
    - **Estresse Médio**: Valores mais altos indicam maior nível de estresse relatado
    - **% Burnout Alto**: Percentual de pessoas com nível alto de burnout no segmento
    - **Horas/Semana**: Média de horas trabalhadas por semana
    
    **Correlações esperadas**:
    - Mais horas → Maior estresse
    - Maior estresse → Maior % burnout
    """)

with col2:
    st.subheader("🎯 Segmentos Disponíveis")
    
    # Informações sobre os tipos de segmento nos dados
    if 'source' in df.columns:
        st.markdown("""
        **Tipos de segmentação por dataset**:
        - `dataset_workplace` → Departamento (HR, IT, Sales, etc.)
        - `dataset_burnout` → Região (Europe, Asia, Americas)
        - `dataset_principal` → Ocupação (Corporate, etc.)
        
        💡 **Dica**: Use os filtros na sidebar para selecionar quais segmentos comparar.
        """)

# Estatísticas detalhadas
st.subheader("📈 Estatísticas Detalhadas")

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
    
    st.dataframe(stats, use_container_width=True)

