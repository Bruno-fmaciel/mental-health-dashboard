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
        df = pd.read_csv(path)
        return _normalize_columns(df, path)
    
    # Caminhos dos seus datasets
    default_paths = [
        "data/dataset_principal.csv",
        "data/dataset_burnout.csv",
        "data/dataset_workplace.csv",
    ]
    
    dfs = []
    for p in default_paths:
        try:
            _df = pd.read_csv(p)
            _df = _normalize_columns(_df, p)
            _df['source'] = p.split('/')[-1].replace('.csv', '')  # Adiciona origem
            dfs.append(_df)
        except Exception as e:
            st.warning(f"Não foi possível carregar {p}: {e}")
            continue
    
    if not dfs:
        st.warning("Nenhum CSV encontrado em /data. Carregando dataframe vazio.")
        return pd.DataFrame()
    
    # Concatena todos os dataframes
    df = pd.concat(dfs, ignore_index=True, sort=False)
    return df


def _normalize_columns(df: pd.DataFrame, filepath: str) -> pd.DataFrame:
    """Normaliza nomes de colunas para o padrão esperado pelos gráficos."""
    df = df.copy()
    
    # Mapeamento baseado no arquivo de origem
    if 'dataset_principal' in filepath:
        # Dataset principal: foco em saúde mental geral
        df['role'] = df.get('Occupation', 'Unknown')
        df['work_mode'] = 'Office'  # Assumir presencial se não especificado
        df['stress_score'] = df['Growing_Stress'].map({'Yes': 8, 'No': 3}).fillna(5)
        df['burnout_level'] = df['Mood_Swings'].map({
            'High': 'high', 'Medium': 'medium', 'Low': 'low'
        }).fillna('medium')
        df['hours_per_week'] = 40  # Padrão se não especificado
        df['policy'] = df['care_options'].fillna('Unknown')
        
    elif 'dataset_burnout' in filepath:
        # Dataset burnout: dados mais completos
        df['role'] = df.get('Job_Role', 'Unknown')
        df['work_mode'] = df.get('Work_Location', 'Unknown')
        df['hours_per_week'] = df.get('Hours_Worked_Per_Week', 40)
        df['stress_score'] = df['Stress_Level'].map({
            'High': 8, 'Medium': 5, 'Low': 2
        }).fillna(5)
        df['burnout_level'] = df['Stress_Level'].map({
            'High': 'high', 'Medium': 'medium', 'Low': 'low'
        }).fillna('medium')
        df['policy'] = df.get('Access_to_Mental_Health_Resources', 'Unknown')
        df['segment'] = df.get('Region', 'Unknown')
        
    elif 'dataset_workplace' in filepath:
        # Dataset workplace: burnout e trabalho remoto
        df['role'] = df.get('JobRole', 'Unknown')
        df['work_mode'] = df.get('RemoteWork', 'Unknown')
        df['hours_per_week'] = df.get('WorkHoursPerWeek', 40)
        df['stress_score'] = df.get('StressLevel', 5)
        df['burnout_level'] = pd.cut(
            df.get('BurnoutLevel', 5),
            bins=[0, 3, 6, 10],
            labels=['low', 'medium', 'high']
        ).astype(str)
        df['policy'] = df.get('HasMentalHealthSupport', 'Unknown').map({
            'Yes': 'With Support', 'No': 'Without Support'
        }).fillna('Unknown')
        df['segment'] = df.get('Department', 'Unknown')
    
    return df


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Cria filtros globais e retorna df filtrado. Reuse em todas as páginas."""
    st.sidebar.header("Filtros")
    
    if df is None or df.empty:
        st.sidebar.info("Carregue dados em /data para ativar filtros.")
        return df
    
    # Obtém valores únicos para os filtros
    roles = sorted(df['role'].dropna().unique()) if 'role' in df.columns else []
    work_modes = sorted(df['work_mode'].dropna().unique()) if 'work_mode' in df.columns else []
    
    # Cria os filtros
    sel_roles = st.sidebar.multiselect("Cargo(s)", roles, default=roles[:3] if roles else [])
    sel_modes = st.sidebar.multiselect("Modalidade", work_modes, default=work_modes if work_modes else [])
    
    # Slider de horas por semana
    if 'hours_per_week' in df.columns and df['hours_per_week'].notna().any():
        min_h = int(df['hours_per_week'].min())
        max_h = int(df['hours_per_week'].max())
        rng_hours = st.sidebar.slider("Horas/semana", min_value=min_h, max_value=max_h, value=(min_h, max_h), key="hours_filter")
    else:
        rng_hours = (0, 100)
    
    # Aplica os filtros
    f = df.copy()
    
    if sel_roles and 'role' in f.columns:
        f = f[f['role'].isin(sel_roles)]
    
    if sel_modes and 'work_mode' in f.columns:
        f = f[f['work_mode'].isin(sel_modes)]
    
    if 'hours_per_week' in f.columns:
        f = f[(f['hours_per_week'] >= rng_hours[0]) & (f['hours_per_week'] <= rng_hours[1])]
    
    st.sidebar.caption(f"📊 {len(f)} de {len(df)} registros selecionados")
    st.sidebar.caption("💡 Dica: refine os filtros conforme suas perguntas de negócio.")
    
    return f