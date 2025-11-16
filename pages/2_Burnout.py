# pages/2_Burnout.py
import streamlit as st
import pandas as pd
from utils.charts import kpi_cards, stacked_env_policies, small_multiples_segments

# ===============================
# CONFIGURAÇÃO VISUAL
# ===============================
st.set_page_config(layout="wide")

st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        h1, h2, h3 {
            font-weight: 600 !important;
            color: #E4E6EB !important;
        }

        [data-testid="stMetricValue"] {
            color: #2980b9;
            font-weight: 600;
        }

        .intro-box {
            background-color: #1B1F24;
            padding: 1.3rem;
            border-radius: 0.5rem;
            border: 1px solid #2a2a2a;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
# TÍTULO E CONTEXTO
# ===============================
st.title("Análise de Esgotamento Profissional (Burnout)")
st.caption("Fatores de estresse, suporte organizacional e impacto no equilíbrio vida-trabalho")

st.markdown("""
<div class='intro-box'>
O conjunto de dados <b>Burnout</b> reúne informações de profissionais de diferentes setores e localizações,
com foco em <b>níveis de estresse, horas de trabalho, satisfação e suporte organizacional</b>.
A análise busca compreender os principais fatores que contribuem para o esgotamento e o bem-estar no ambiente corporativo.
</div>
""", unsafe_allow_html=True)

# ===============================
# CARREGAMENTO DE DADOS
# ===============================
@st.cache_data
def carregar_burnout():
    return pd.read_csv("data/dataset_burnout.csv")

df = carregar_burnout()

# ===============================
# KPIs GERAIS
# ===============================
st.markdown("### Indicadores-Chave — Esgotamento e Estresse")
kpi_cards(df)

st.markdown("---")

# ===============================
# POLÍTICAS E SUPORTE ORGANIZACIONAL
# ===============================
st.markdown("### Políticas Organizacionais e Saúde Mental")
try:
    fig_policy = stacked_env_policies(df, title="Recursos de Saúde Mental vs Nível de Estresse")
    st.plotly_chart(fig_policy, use_container_width=True)
except Exception as e:
    st.warning(f"Não foi possível gerar o gráfico de políticas: {e}")

st.markdown("---")

# ===============================
# TENDÊNCIAS POR INDÚSTRIA E REGIÃO
# ===============================
st.markdown("### Tendências de Burnout por Indústria e Região")

col1, col2 = st.columns(2)

with col1:
    try:
        fig_industry = small_multiples_segments(df, top_n=8, title="Média de Estresse/Burnout por Indústria")
        st.plotly_chart(fig_industry, use_container_width=True)
    except Exception as e:
        st.warning(f"Erro ao gerar gráfico por indústria: {e}")

with col2:
    try:
        if "Region" in df.columns:
            tmp = df.groupby("Region")["Stress_Level"].mean().reset_index().sort_values("Stress_Level", ascending=False)
            import plotly.express as px
            fig_region = px.bar(tmp, x="Region", y="Stress_Level",
                                title="Média de Estresse por Região",
                                labels={"Region": "Região", "Stress_Level": "Média de Estresse"},
                                text_auto=".2f")
            fig_region.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig_region, use_container_width=True)
    except Exception as e:
        st.warning(f"Erro ao gerar gráfico por região: {e}")

st.markdown("---")

# ===============================
# CORRELAÇÕES ENTRE VARIÁVEIS
# ===============================
st.markdown("### Correlação entre Fatores de Trabalho e Estresse")

try:
    numeric_cols = df.select_dtypes(include="number").columns
    if "Stress_Level" in numeric_cols:
        import seaborn as sns
        import matplotlib.pyplot as plt

        corr = df[numeric_cols].corr()["Stress_Level"].sort_values(ascending=False)
        top_corr = corr.head(8)

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=top_corr.values, y=top_corr.index, palette="Blues_d", ax=ax)
        ax.set_title("Correlação com o Nível de Estresse", color="#E4E6EB", fontsize=12)
        ax.set_xlabel("Correlação", color="#E4E6EB")
        ax.set_ylabel("")
        ax.tick_params(colors="#E4E6EB")
        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")
        st.pyplot(fig)
except Exception as e:
    st.warning(f"Erro ao gerar gráfico de correlação: {e}")

st.markdown("---")

# ===============================
# INTERPRETAÇÃO
# ===============================
st.markdown("""
<div class='intro-box'>
<b>Interpretação:</b>  
Os resultados sugerem que altos níveis de estresse estão frequentemente associados a:
<ul>
<li>Jornadas de trabalho mais longas e menor equilíbrio vida-trabalho;</li>
<li>Baixo suporte organizacional e acesso limitado a recursos de saúde mental;</li>
<li>Diferenças entre setores — indústrias mais competitivas apresentam médias mais altas de burnout;</li>
<li>Regiões com menor suporte social tendem a concentrar níveis de estresse mais elevados.</li>
</ul>
Esses padrões indicam a importância de políticas internas e programas de bem-estar corporativo
para reduzir os riscos de esgotamento entre profissionais.
</div>
""", unsafe_allow_html=True)
