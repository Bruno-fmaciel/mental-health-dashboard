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
    
    # Criar age_group se Age existir
    if 'Age' in df.columns:
        df['age_group'] = pd.cut(
            df['Age'],
            bins=[0, 30, 40, 50, 100],
            labels=['18-30', '31-40', '41-50', '50+']
        ).astype(str)
    
    # Normaliza Gender para lowercase para consistência
    if 'Gender' in df.columns:
        df['gender'] = df['Gender'].str.lower()
    
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


def render_sidebar(df: pd.DataFrame, show_segment_filter: bool = False) -> pd.DataFrame:
    """Cria filtros globais e retorna df filtrado. Reuse em todas as páginas.
    
    Args:
        df: DataFrame com os dados
        show_segment_filter: Se True, mostra filtro adicional de segmentos (útil para página de Perfis)
    
    Returns:
        DataFrame filtrado
    """
    st.sidebar.header("🎯 Filtros")
    
    if df is None or df.empty:
        st.sidebar.info("Carregue dados em /data para ativar filtros.")
        return df
    
    # =====================================
    # BLOCO 1: 👥 QUEM VOCÊ QUER ANALISAR?
    # =====================================
    st.sidebar.subheader("👥 Quem você quer analisar?")
    st.sidebar.caption("Escolha o perfil dos profissionais. Diferentes cargos e segmentos podem apresentar padrões distintos de estresse e burnout.")
    
    # Obtém valores únicos para os filtros
    roles = sorted(df['role'].dropna().unique()) if 'role' in df.columns else []
    segments = sorted(df['segment'].dropna().unique()) if 'segment' in df.columns else []
    
    # Filtro de cargos - TODOS selecionados por padrão
    sel_roles = st.sidebar.multiselect(
        "Cargo(s)",
        roles,
        default=roles,  # MUDANÇA: todos selecionados
        help="Diferentes ocupações podem ter níveis variados de risco de burnout. Exemplo: cargos com alta responsabilidade ou longas jornadas tendem a apresentar mais estresse.",
        key="filter_roles"
    )
    
    # Filtro de segmentos (opcional, apenas na página de Perfis)
    if show_segment_filter and segments:
        # Pega os 4 segmentos mais frequentes como default
        top_segments = df['segment'].value_counts().nlargest(4).index.tolist()
        
        sel_segments = st.sidebar.multiselect(
            "Segmentos (Depto/Região)",
            segments,
            default=top_segments,
            help="Compare departamentos (IT, HR, Sales) ou regiões (Americas, Europe, Asia). Isso ajuda a identificar onde o burnout é mais prevalente na organização.",
            key="filter_segments"
        )
    else:
        sel_segments = []
    
    # =====================================
    # BLOCO 2: 💼 COMO ESSAS PESSOAS TRABALHAM?
    # =====================================
    st.sidebar.divider()
    st.sidebar.subheader("💼 Como essas pessoas trabalham?")
    st.sidebar.caption("A modalidade de trabalho pode influenciar o equilíbrio vida-trabalho e o risco de burnout. Compare presencial, remoto e híbrido.")
    
    work_modes = sorted(df['work_mode'].dropna().unique()) if 'work_mode' in df.columns else []
    
    sel_modes = st.sidebar.multiselect(
        "Modalidade de Trabalho",
        work_modes,
        default=work_modes,  # TODOS selecionados por padrão
        help="Remoto pode aumentar isolamento social; presencial pode gerar estresse por deslocamento; híbrido pode criar sobrecarga de transição. Use para comparar padrões.",
        key="filter_modes"
    )
    
    # =====================================
    # BLOCO 3: ⏱️ QUAL A CARGA DE TRABALHO?
    # =====================================
    st.sidebar.divider()
    st.sidebar.subheader("⏱️ Qual a carga de trabalho?")
    st.sidebar.caption("Longas jornadas (>40h/semana) são um fator de risco conhecido para burnout. Filtre para identificar grupos mais vulneráveis.")
    
    # Slider de horas por semana
    if 'hours_per_week' in df.columns and df['hours_per_week'].notna().any():
        min_h = int(df['hours_per_week'].min())
        max_h = int(df['hours_per_week'].max())
        rng_hours = st.sidebar.slider(
            "Horas trabalhadas/semana",
            min_value=min_h,
            max_value=max_h,
            value=(min_h, max_h),  # Range completo por padrão
            help="Horas trabalhadas por semana. Valores acima de 40-45h estão associados a maior risco de esgotamento, estresse crônico e problemas de saúde mental.",
            key="hours_filter"
        )
    else:
        rng_hours = (0, 100)
    
    # =====================================
    # APLICAR FILTROS
    # =====================================
    f = df.copy()
    
    if sel_roles and 'role' in f.columns:
        f = f[f['role'].isin(sel_roles)]
    
    if sel_modes and 'work_mode' in f.columns:
        f = f[f['work_mode'].isin(sel_modes)]
    
    if sel_segments and 'segment' in f.columns:
        f = f[f['segment'].isin(sel_segments)]
    
    if 'hours_per_week' in f.columns:
        f = f[(f['hours_per_week'] >= rng_hours[0]) & (f['hours_per_week'] <= rng_hours[1])]
    
    # =====================================
    # RESUMO DOS FILTROS APLICADOS
    # =====================================
    st.sidebar.divider()
    st.sidebar.caption(f"📊 **{len(f):,}** de **{len(df):,}** registros selecionados")
    
    # Gera descrição contextual dos filtros
    descricao_partes = []
    
    if sel_roles and len(sel_roles) < len(roles):
        if len(sel_roles) <= 3:
            descricao_partes.append(f"**{', '.join(sel_roles)}**")
        else:
            descricao_partes.append(f"**{len(sel_roles)} cargos selecionados**")
    
    if sel_modes and len(sel_modes) < len(work_modes):
        if len(sel_modes) <= 2:
            descricao_partes.append(f"modalidade **{' ou '.join(sel_modes)}**")
        else:
            descricao_partes.append(f"**{len(sel_modes)} modalidades**")
    
    if rng_hours[0] > min_h or rng_hours[1] < max_h:
        descricao_partes.append(f"**{rng_hours[0]}-{rng_hours[1]}h/semana**")
    
    if descricao_partes:
        descricao = "Você está vendo: " + ", ".join(descricao_partes) + "."
        st.sidebar.caption(descricao)
    else:
        st.sidebar.caption("Você está vendo: **todos os dados** (sem filtros ativos).")
    
    st.sidebar.caption("💡 **Dica de análise**: Explore combinações de filtros para responder perguntas como: 'Desenvolvedores remotos com >50h/semana têm mais burnout?' ou 'Qual departamento apresenta maior risco?'")
    
    return f