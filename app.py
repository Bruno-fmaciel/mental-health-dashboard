import streamlit as st
import pandas as pd
from utils.data_io import load_data, render_sidebar
from utils.theming import set_page_theme

# Configuração básica da página
st.set_page_config(
    page_title="Mental Health — Dashboard SR2",
    page_icon="🧠",
    layout="wide"
)
set_page_theme()

# Carrega dados (ajuste o caminho ou fonte em utils/data_io.py)
df = load_data()

# Sidebar global (filtros compartilhados)
filtered = render_sidebar(df)

st.title("🧠 Mental Health — Dashboard SR2")
st.caption("Home • Use o menu lateral para navegar pelas páginas.")

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Status")
    st.markdown("""
    - ✅ Estrutura multipágina criada
    - ✅ Filtros globais na sidebar
    - 🧩 Complete gráficos nas páginas em `pages/`
    - 📄 Ajuste o texto em **Sobre & Métodos**
    """)

with col2:
    st.subheader("Dados carregados (amostra)")
    st.dataframe(filtered.head(20), use_container_width=True)

st.divider()
st.markdown("**Próximos passos:** criar *Issues* no GitHub para cada TODO e relacione às páginas.")