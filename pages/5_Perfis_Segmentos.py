import streamlit as st
from utils.data_io import load_data, render_sidebar
from utils.charts import small_multiples_segments

st.set_page_config(page_title="Perfis & Segmentos — SR2", page_icon="🧩", layout="wide")

st.title("🧩 Perfis & Segmentos")
df = load_data()
df = render_sidebar(df)

st.subheader("Comparações entre segmentos")
st.plotly_chart(small_multiples_segments(df), use_container_width=True, key="small_multiples_segments")

st.info("TODO: definir segmentos prioritários (ex.: squad, senioridade, região).")

