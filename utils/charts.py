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
    """
    Cria gráficos de comparação entre segmentos (departamentos/regiões).
    
    Mostra múltiplas métricas por segmento:
    - Estresse médio
    - % Burnout Alto
    - Horas médias por semana
    """
    if df is None or df.empty or 'segment' not in df.columns:
        return go.Figure()
    
    # Agrupa por segmento e calcula métricas
    metrics = df.groupby('segment').agg({
        'stress_score': 'mean',
        'hours_per_week': 'mean',
        'segment': 'count'  # contagem
    }).rename(columns={'segment': 'count'})
    
    # Calcula % de burnout alto
    if 'burnout_level' in df.columns:
        burnout_high = df[df['burnout_level'] == 'high'].groupby('segment').size()
        metrics['pct_high_burnout'] = (burnout_high / metrics['count'] * 100).fillna(0)
    else:
        metrics['pct_high_burnout'] = 0
    
    metrics = metrics.reset_index()
    
    # Cria figura com subplots
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Estresse Médio', '% Burnout Alto', 'Horas/Semana Médias'),
        horizontal_spacing=0.1
    )
    
    # Gráfico 1: Estresse médio
    fig.add_trace(
        go.Bar(
            x=metrics['segment'],
            y=metrics['stress_score'],
            name='Estresse',
            marker_color='#FF6B6B',
            text=metrics['stress_score'].round(1),
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Gráfico 2: % Burnout alto
    fig.add_trace(
        go.Bar(
            x=metrics['segment'],
            y=metrics['pct_high_burnout'],
            name='% Burnout Alto',
            marker_color='#EE5A6F',
            text=metrics['pct_high_burnout'].round(1).astype(str) + '%',
            textposition='outside'
        ),
        row=1, col=2
    )
    
    # Gráfico 3: Horas médias
    fig.add_trace(
        go.Bar(
            x=metrics['segment'],
            y=metrics['hours_per_week'],
            name='Horas/Sem',
            marker_color='#4ECDC4',
            text=metrics['hours_per_week'].round(1),
            textposition='outside'
        ),
        row=1, col=3
    )
    
    fig.update_layout(
        title_text="Comparação de Métricas por Segmento",
        showlegend=False,
        height=400
    )
    
    fig.update_yaxes(title_text="Nível", row=1, col=1)
    fig.update_yaxes(title_text="Percentual", row=1, col=2)
    fig.update_yaxes(title_text="Horas", row=1, col=3)
    
    return fig