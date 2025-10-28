import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def kpi_cards(df: pd.DataFrame):
    import streamlit as st
    if df is None or df.empty:
        st.info("Sem dados para KPIs.")
        return
    # TODO: troque as métricas para suas regras
    n_resp = len(df)
    pct_risco = (df['burnout_level'].isin(['high', 'alto']).mean()*100) if 'burnout_level' in df.columns else 0
    avg_stress = df['stress_score'].mean() if 'stress_score' in df.columns else 0
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Respondentes", f"{n_resp:,}")
    c2.metric("% Risco Burnout", f"{pct_risco:.1f}%")
    c3.metric("Estresse médio", f"{avg_stress:.1f}")


def dist_stress(df: pd.DataFrame):
    if df is None or df.empty or 'stress_score' not in df.columns:
        return go.Figure()
    fig = px.histogram(df, x='stress_score', nbins=20, marginal="box")
    fig.update_layout(title="Distribuição do Estresse", xaxis_title="Escore de estresse", yaxis_title="Contagem")
    return fig


def scatter_hours_burnout(df: pd.DataFrame):
    if df is None or df.empty or not set(['hours_per_week', 'stress_score']).issubset(df.columns):
        return go.Figure()
    color = 'burnout_level' if 'burnout_level' in df.columns else None
    fig = px.scatter(df, x='hours_per_week', y='stress_score', color=color, trendline="ols")
    fig.update_layout(title="Horas/semana × Estresse")
    fig.update_xaxes(title="Horas por semana")
    fig.update_yaxes(title="Escore de estresse")
    return fig


def box_burnout_by_role(df: pd.DataFrame):
    cols = ['role', 'stress_score']
    if df is None or df.empty or not set(cols).issubset(df.columns):
        return go.Figure()
    fig = px.box(df, x='role', y='stress_score', points='all')
    fig.update_layout(title="Estresse por Cargo/Modalidade", xaxis_title="Cargo", yaxis_title="Estresse")
    return fig


def stacked_env_policies(df: pd.DataFrame):
    # TODO: ajuste estas colunas às suas políticas/variáveis ambientais
    if df is None or df.empty:
        return go.Figure()
    # Exemplo mínimo: contar respostas por 'policy' × 'burnout_level'
    if not set(['policy', 'burnout_level']).issubset(df.columns):
        return go.Figure()
    ct = df.groupby(['policy', 'burnout_level']).size().reset_index(name='n')
    fig = px.bar(ct, x='policy', y='n', color='burnout_level', barmode='stack')
    fig.update_layout(title="Políticas × Burnout", xaxis_title="Política", yaxis_title="Respostas")
    return fig


def violin_by_workmode(df: pd.DataFrame):
    if df is None or df.empty or not set(['work_mode', 'stress_score']).issubset(df.columns):
        return go.Figure()
    fig = px.violin(df, x='work_mode', y='stress_score', box=True, points='all')
    fig.update_layout(title="Estresse por Modalidade de Trabalho", xaxis_title="Modalidade", yaxis_title="Estresse")
    return fig


def small_multiples_segments(df: pd.DataFrame):
    # TODO: ajuste segmento (ex.: 'region' ou 'seniority') e métrica
    if df is None or df.empty:
        return go.Figure()
    seg = 'segment' if 'segment' in df.columns else None
    if not seg or 'stress_score' not in df.columns:
        return go.Figure()
    fig = px.bar(df, x=seg, y='stress_score', facet_col=seg)
    fig.update_layout(title="Comparações entre Segmentos")
    return fig