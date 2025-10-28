import streamlit as st

st.set_page_config(page_title="Sobre & Métodos — SR2", page_icon="ℹ️", layout="wide")

st.title("ℹ️ Sobre & Métodos")

st.markdown(
    """
    ### Problema & Perguntas de Negócio
    - **Problema**: TODO
    - **Perguntas**: TODO (liste 3–5 perguntas que o dashboard responde)

    ### Dados & Preparação
    - Fonte(s): TODO
    - Limpeza/Tratamento: TODO
    - Limitações: TODO

    ### Metodologias
    - **CRISP-DM**: entendimento do negócio → entendimento dos dados → preparação → modelagem/visualização → avaliação → implantação (dashboard)
    - **Storytelling com Dados**: gráficos com título que responde "o que vejo" + anotações de insight
    - **Design de Dashboards**: foco no usuário/decisão; interações e contexto

    ### Time & Artefatos
    - Repositório, Slides, Site, URL do Dashboard: TODO (insira links)
    """
)

