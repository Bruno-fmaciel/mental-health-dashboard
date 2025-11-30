import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.theming import set_page_theme
from utils.charts import (
    make_workmode_kpi_cards,
    plot_stress_by_workmode,
    plot_burnout_by_workmode,
    plot_workmode_delta_heatmap
)

st.set_page_config(layout="wide", page_title="Modalidades de Trabalho")
set_page_theme()

# ====================================
# CARREGA E FILTRA DADOS
# ====================================
df = load_data()
filtered = render_sidebar(df)

# Validação de DataFrame vazio
if filtered.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# ====================================
# HERO SECTION
# ====================================
st.title("Modalidades de trabalho")
st.caption("Comparação entre remoto, híbrido e presencial em estresse e burnout.")

# ====================================
# KPIs PER WORK MODE
# ====================================
workmode_stats = make_workmode_kpi_cards(filtered)

if workmode_stats and len(workmode_stats) > 0:
    cols = st.columns(len(workmode_stats))
    for idx, (mode, stats) in enumerate(workmode_stats.items()):
        with cols[idx] if idx < len(cols) else st.container():
            st.metric(
                f"{mode.capitalize()}",
                f"{stats.get('high_burnout_pct', 0):.1f}%",
                delta=f"Estresse: {stats.get('avg_stress', 0):.1f}"
            )
else:
    st.info("ℹ️ Dados de modalidades de trabalho não disponíveis.")

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 1: STRESS BY WORK MODE
# ====================================
st.plotly_chart(plot_stress_by_workmode(filtered), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 2: BURNOUT BY WORK MODE
# ====================================
st.plotly_chart(plot_burnout_by_workmode(filtered), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 3: ADVANCED / EXPLORATORY SECTION
# ====================================
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
st.subheader("Análise avançada: deltas de risco por modalidade")
st.caption("Comparação detalhada de diferenças de risco entre modalidades por segmento.")

# Identify available segmentation columns
available_segments = []
segment_labels = {
    'segment': 'Região',
    'role': 'Ocupação (principal)',
    'policy': 'Política'
}

for col in ['segment', 'role', 'policy']:
    if col in filtered.columns and filtered[col].notna().sum() > 10:
        available_segments.append(col)

if available_segments:
    col1, col2 = st.columns(2)
    
    with col1:
        segment_dim = st.selectbox(
            "Dimensão de segmentação:",
            options=available_segments,
            format_func=lambda x: segment_labels.get(x, x)
        )
    
    with col2:
        delta_type = st.selectbox(
            "Tipo de delta:",
            options=["Remoto − Híbrido", "Remoto − Presencial", "Híbrido − Presencial"]
        )
    
    fig = plot_workmode_delta_heatmap(filtered, segment_dim, delta_type)
    st.plotly_chart(fig, use_container_width=True)
    
    # Add explanation as caption below the chart
    mode1, mode2 = delta_type.split(' − ')
    st.caption(
        f"💡 **Interpretação**: Valores positivos indicam que {mode1.strip()} tem maior risco que {mode2.strip()}. "
        f"Valores negativos indicam que {mode2.strip()} tem maior risco que {mode1.strip()}."
    )
else:
    st.info("ℹ️ Não há dimensões de segmentação suficientes para análise avançada.")

# ====================================
# FOOTER
# ====================================
st.markdown("<br><hr><center style='color:gray'>Dashboard • Projetos 5 — GTI • 2025</center>",
            unsafe_allow_html=True)
