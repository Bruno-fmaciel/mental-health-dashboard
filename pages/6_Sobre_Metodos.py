import streamlit as st
import pandas as pd
from utils.data_io import load_data

st.set_page_config(page_title="Sobre & Métodos — SR2", page_icon="ℹ️", layout="wide")

st.title("ℹ️ Sobre & Métodos")

# ============================
# Resumo Automático (C9)
# ============================

st.subheader("📝 Resumo Automático do Dashboard")

df = load_data()

if df is None or df.empty:
    st.warning("Não foi possível gerar o resumo automático. O dataset está vazio.")
else:
    # -------- NORMALIZAÇÃO DAS MODALIDADES DE TRABALHO -------- #
    # Converte valores variados para 3 categorias finais:
    # remote / hybrid / onsite
    map_modes = {
        "remote": "remote",
        "yes": "remote",

        "hybrid": "hybrid",

        "office": "onsite",
        "onsite": "onsite",
        "no": "onsite"
    }

    df["work_mode_norm"] = (
        df["work_mode"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(map_modes)
        .fillna("unknown")
    )

    # Quantidade de respondentes
    total = len(df)

    # Modalidades normalizadas
    modalidades = df["work_mode_norm"].value_counts()

    # Média geral de estresse
    stress_mean = df["stress_score"].mean()

    # Horas semanais
    hours_mean = df["hours_per_week"].mean()

    # Burnout (se existir)
    burnout_info = ""
    if "burnout_level" in df.columns:
        counts = df["burnout_level"].value_counts(normalize=True) * 100
        burnout_info = (
            f"- **{counts.get('high', 0):.1f}%** apresentam *alto burnout*\n"
            f"- **{counts.get('medium', 0):.1f}%** burnout moderado\n"
        )

    resumo = f"""
### 📌 Principais Achados dos Dados

Com base nos dados integrados utilizados no dashboard:

- O dataset contém **{total} respondentes** provenientes de diferentes fontes.
- A distribuição das modalidades de trabalho é:
    - **{modalidades.get('remote', 0)}** trabalhadores remotos  
    - **{modalidades.get('hybrid', 0)}** trabalhadores híbridos  
    - **{modalidades.get('onsite', 0)}** trabalhadores presenciais  
- O nível médio de estresse geral é **{stress_mean:.2f}**.
- A carga horária semanal média aproximada é de **{hours_mean:.1f} horas**.

### 🔥 Indicadores Gerais de Burnout
{burnout_info or "- O dataset não possui a variável `burnout_level`."}

Esses resultados fornecem o contexto necessário para entender as análises detalhadas apresentadas nas páginas seguintes.
"""

    st.info(resumo)


# ======================================================
# Página fixa (metodologia, dados, storytelling etc.)
# ======================================================

st.markdown("""
### 🎯 Problema & Perguntas de Negócio

**Problema**: 
TODO: Descreva o problema de negócio que o dashboard aborda.

*Exemplo*: Como a transição para trabalho remoto/híbrido impactou a saúde mental 
dos trabalhadores? Quais fatores organizacionais podem mitigar o burnout?

**Perguntas de Pesquisa**:
1. TODO: Primeira pergunta que o dashboard responde
2. TODO: Segunda pergunta que o dashboard responde
3. TODO: Terceira pergunta que o dashboard responde
4. TODO: Quarta pergunta que o dashboard responde (opcional)
5. TODO: Quinta pergunta que o dashboard responde (opcional)

---

### 📊 Dados & Preparação

**Fontes dos Dados**:

TODO: Descreva as fontes dos dados

*Template*:
- **Dataset Principal** – Saúde mental no trabalho  
- **Dataset Burnout** – Burnout e estresse ocupacional  
- **Dataset Workplace** – Ambiente, políticas e satisfação  

**Limpeza e Tratamento**:
- Normalização de colunas (role, work_mode, stress_score)
- Conversão de categorias de estresse
- Criação de burnout_level
- Remoção de valores ausentes críticos

**Limitações**:
- Dados auto-reportados
- Diferenças entre datasets
- Ausência de dados longitudinais
- Possível não representatividade

---

### 🔬 Metodologias

#### CRISP-DM
- Entendimento do Negócio  
- Entendimento dos Dados  
- Preparação  
- Modelagem / Visualização  
- Avaliação  
- Deploy  

#### Storytelling com Dados
- Narrativa clara  
- Gráficos com títulos interpretativos  
- Destaques de insights  
- Paleta consistente  

#### Design do Dashboard
- Foco no usuário  
- KPIs no topo  
- Comparações diretas  
- Interatividade (Plotly)  
- Responsividade (wide layout)  

---

### 👥 Time & Artefatos

**Equipe**:
- Bruno Maciel (GitHub: @Bruno-fmaciel)
- Camila Oliveira

**Artefatos do Projeto**:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
#### 🔗 Links Principais
- **Repositório GitHub**: https://github.com/Bruno-fmaciel/mental-health-dashboard
- **Dashboard**: TODO
- **Slides**: TODO
""")

with col2:
    st.markdown("""
#### 📚 Recursos
- Google Site: TODO
- Documentação: README
- Licença: MIT
""")

st.divider()

st.markdown("""
### 📖 Referências

TODO: Adicione as referências bibliográficas utilizadas
""")

st.info("💡 Atualize esta página conforme o projeto evolui. Ela é essencial para o SR2!")
