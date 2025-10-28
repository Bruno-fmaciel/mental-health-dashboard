import streamlit as st
import pandas as pd
from typing import Optional


@st.cache_data(show_spinner=False)
def load_data(path: Optional[str] = None) -> pd.DataFrame:
    """Carrega dados a partir de CSV(s).
    - Ajuste o caminho padrão e/ou substitua por leitura de múltiplos arquivos.
    - Garanta que os nomes de colunas usados em utils/charts.py existam.
    """
    if path:
        return pd.read_csv(path)
    default_paths = [
        "data/merged_mental_health_remote_burnout.csv",
        "data/mental_health_remote_workers.csv",
        "data/mental_health_workplace_survey.csv",
    ]
    df = None
    paths = [path] if path else default_paths
    for p in paths:
        try:
            _df = pd.read_csv(p)
            df = _df if df is None else pd.concat([df, _df], ignore_index=True)
        except Exception:
            continue
    if df is None or df.empty:
        st.warning("Nenhum CSV encontrado em /data. Carregando dataframe vazio.")
        df = pd.DataFrame()

    # TODO: renomeie/normalize colunas conforme necessário
    # Exemplo esperado pelas funções de chart:
    # - 'stress_score', 'burnout_level', 'hours_per_week', 'role', 'work_mode'
    return df


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Cria filtros globais e retorna df filtrado. Reuse em todas as páginas."""
    if df is None or df.empty:
        st.sidebar.info("Carregue dados em /data para ativar filtros.")
        return df
    st.sidebar.header("Filtros")
    roles = sorted(df['role'].dropna().unique()) if 'role' in df.columns else []
    work_modes = sorted(df['work_mode'].dropna().unique()) if 'work_mode' in df.columns else []
    min_h, max_h = (int(df['hours_per_week'].min()), int(df['hours_per_week'].max())) if 'hours_per_week' in df.columns and df['hours_per_week'].notna().any() else (0, 100)
    rng_hours = st.sidebar.slider("Horas/semana", min_value=min_h, max_value=max_h, value=(min_h, max_h))
    f = df.copy()
    if df is None or df.empty:
        st.sidebar.info("Carregue dados em /data para ativar filtros.")
        return df
    sel_roles = st.sidebar.multiselect("Cargo(s)", roles, default=roles[:3] if roles else [])
    sel_modes = st.sidebar.multiselect("Modalidade", work_modes, default=work_modes if work_modes else [])
    min_h, max_h = (int(df['hours_per_week'].min()), int(df['hours_per_week'].max())) if 'hours_per_week' in df.columns and df['hours_per_week'].notna().any() else (0, 100)
    rng_hours = st.sidebar.slider("Horas/semana", min_value=min_h, max_value=max_h, value=(min_h, max_h))
    f = df.copy()
    if sel_roles and 'role' in f.columns:
        f = f[f['role'].isin(sel_roles)]
    if sel_modes and 'work_mode' in f.columns:
        f = f[f['work_mode'].isin(sel_modes)]
    if 'hours_per_week' in f.columns:
        f = f[(f['hours_per_week'] >= rng_hours[0]) & (f['hours_per_week'] <= rng_hours[1])]
    st.sidebar.caption("Dica: refine ou adicione filtros conforme suas perguntas de negócio.")
    return f