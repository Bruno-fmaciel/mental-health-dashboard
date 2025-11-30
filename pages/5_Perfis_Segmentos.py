import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.theming import set_page_theme
from utils.charts import (
    make_segments_kpi_cards,
    plot_segment_burnout_ranking,
    plot_segment_stress_mean,
    make_segment_summary_table
)

st.set_page_config(page_title="Perfis & Segmentos — SR2", page_icon="🧩", layout="wide")
set_page_theme()

# ====================================
# CARREGA E FILTRA DADOS
# ====================================
df = load_data()
df_filtered = render_sidebar(df, show_segment_filter=True)

# Verifica se há dados após filtros
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado disponível com os filtros selecionados. Ajuste os filtros na sidebar.")
    st.stop()

# ====================================
# HERO SECTION
# ====================================
st.title("Perfis & segmentos")
st.caption("Identificação de grupos com maior estresse e burnout.")

# ====================================
# SEGMENTATION SELECTBOX
# ====================================
# Determine available segmentation columns
available_segmentations = []
segmentation_labels = {
    'segment': 'Região',
    'role': 'Ocupação (principal)',
    'policy': 'Política'
}

for col in ['segment', 'role', 'policy']:
    if col in df_filtered.columns and df_filtered[col].notna().sum() > 5:
        available_segmentations.append(col)

if not available_segmentations:
    st.error("❌ Nenhuma dimensão de segmentação disponível nos dados filtrados.")
    st.stop()

segmentation = st.selectbox(
    "Tipo de segmentação:",
    options=available_segmentations,
    format_func=lambda x: segmentation_labels.get(x, x)
)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# KPIs
# ====================================
n_segments, pct_critical, overall_high_burnout = make_segments_kpi_cards(df_filtered, segmentation)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Segmentos", n_segments)

with col2:
    st.metric(
        "% em Segmentos Críticos",
        f"{pct_critical:.1f}%",
        help="Top 3 segmentos por % de burnout alto"
    )

with col3:
    st.metric("% Burnout Alto Geral", f"{overall_high_burnout:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 1: SEGMENT BURNOUT RANKING
# ====================================
st.plotly_chart(plot_segment_burnout_ranking(df_filtered, segmentation), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 2: SEGMENT STRESS MEAN
# ====================================
st.plotly_chart(plot_segment_stress_mean(df_filtered, segmentation), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================
# BLOCK 3: SUMMARY DATAFRAME
# ====================================
summary_df = make_segment_summary_table(df_filtered, segmentation)
if not summary_df.empty:
    st.dataframe(summary_df, use_container_width=True)

# ====================================
# FOOTER
# ====================================
st.markdown("<br><hr><center style='color:gray'>Dashboard • Projetos 5 — GTI • 2025</center>",
            unsafe_allow_html=True)
