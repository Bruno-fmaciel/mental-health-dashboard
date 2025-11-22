import numpy as np
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

def _ensure_categories(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
    return df

def compute_risk_delta_by_mode_segment(
    df: pd.DataFrame,
    segment_col: str,
    mode_col: str = "work_mode",
    risk_metric: str = "burnout_high",       # "burnout_high" | "stress_threshold"
    stress_col: str = "stress_score",
    stress_threshold: float = 7.0,
    burnout_col: str = "burnout_level",
    burnout_high_value: str = "high",
    min_n: int = 15                           # filtra categorias com pouca amostra
) -> pd.DataFrame:
    """
    Retorna tabela com risco por Remote/Hybrid e delta = Remote - Hybrid para cada valor do segmento.
    """
    req_cols = [segment_col, mode_col]
    if risk_metric == "burnout_high":
        req_cols.append(burnout_col)
    else:
        req_cols.append(stress_col)
    for c in req_cols:
        if c not in df.columns:
            raise ValueError(f"Coluna necessária ausente: {c}")

    df = df.copy()
    df = _ensure_categories(df, [segment_col, mode_col])

    # define flag de risco
    if risk_metric == "burnout_high":
        df["_risk_flag"] = (df[burnout_col].astype(str).str.lower() == str(burnout_high_value).lower())
    else:
        df["_risk_flag"] = pd.to_numeric(df[stress_col], errors="coerce") >= stress_threshold

    # somente Remote/Hybrid
    df = df[df[mode_col].isin(["Remote", "Hybrid"])]

    # agrupa
    g = (
        df.groupby([segment_col, mode_col], dropna=False)
          .agg(n=(" _risk_flag".strip(), "size"), risk=(" _risk_flag".strip(), "mean"))
          .reset_index()
    )

    # reshape wide
    wide = g.pivot(index=segment_col, columns=mode_col, values=["risk","n"]).fillna(0)
    # flatten columns
    wide.columns = [f"{a}_{b}" for a,b in wide.columns]
    for col in ["risk_Hybrid","risk_Remote","n_Hybrid","n_Remote"]:
        if col not in wide.columns:
            wide[col] = 0.0

    wide = wide.reset_index()

    # aplica mínimo de amostra
    wide["n_min"] = wide[["n_Hybrid","n_Remote"]].min(axis=1)
    wide = wide[wide["n_min"] >= min_n].copy()

    # delta
    wide["delta"] = wide["risk_Remote"] - wide["risk_Hybrid"]
    wide["risk_Remote_pct"] = (wide["risk_Remote"]*100).round(1)
    wide["risk_Hybrid_pct"] = (wide["risk_Hybrid"]*100).round(1)
    wide["delta_pct"] = (wide["delta"]*100).round(1)
    return wide.sort_values("delta", ascending=False)

def plot_risk_bars_remote_hybrid(df_delta: pd.DataFrame, segment_col: str):
    long = df_delta[[segment_col,"risk_Remote","risk_Hybrid"]].melt(
        id_vars=segment_col, var_name="mode", value_name="risk"
    )
    long["risk_pct"] = (long["risk"]*100).round(1)
    fig = px.bar(
        long, x=segment_col, y="risk_pct", color="mode",
        barmode="group",
        labels={"risk_pct":"Risco (%)","mode":"Modalidade"},
        title="Risco por Modalidade (Remote x Hybrid)"
    )
    fig.update_layout(xaxis_title=segment_col, legend_title="Modalidade")
    return fig

def plot_delta_lollipop(df_delta: pd.DataFrame, segment_col: str):
    # lollipop = linha do 0 até delta, com marcador na ponta
    base = px.scatter(
        df_delta, x="delta_pct", y=segment_col,
        labels={"delta_pct":"Delta Remoto − Híbrido (pp)"},
        title="Delta de Risco por Segmento (positivo = Remoto pior)"
    )
    for i, row in df_delta.iterrows():
        base.add_shape(
            type="line",
            x0=0, x1=row["delta_pct"],
            y0=i+1, y1=i+1,
            line=dict(width=2)
        )
    return base

def plot_delta_heatmap(
    df: pd.DataFrame,
    rows_col: str, cols_col: str,
    mode_col: str = "work_mode",
    **kwargs
):
    """Heatmap de delta por 2 dimensões de segmento."""
    d = compute_risk_delta_by_mode_segment(df, segment_col=rows_col, mode_col=mode_col, **kwargs)
    d2 = compute_risk_delta_by_mode_segment(df, segment_col=cols_col, mode_col=mode_col, **kwargs)
    # junta pelo cartesian? melhor recalcular usando ambos:
    df = df[df[mode_col].isin(["Remote","Hybrid"])].copy()
    df["_risk_flag"] = (
        (df.get(kwargs.get("burnout_col","burnout_level"),"").astype(str).str.lower() == str(kwargs.get("burnout_high_value","high")).lower())
        if kwargs.get("risk_metric","burnout_high") == "burnout_high"
        else pd.to_numeric(df.get(kwargs.get("stress_col","stress_score")), errors="coerce") >= kwargs.get("stress_threshold",7.0)
    )
    g = (
        df.groupby([rows_col, cols_col, mode_col])
          .agg(risk=("_risk_flag","mean"), n=("_risk_flag","size"))
          .reset_index()
    )
    wide = g.pivot_table(index=[rows_col, cols_col], columns=mode_col, values="risk").reset_index()
    for m in ["Remote","Hybrid"]:
        if m not in wide.columns: wide[m]=np.nan
    wide["delta_pct"] = ((wide["Remote"] - wide["Hybrid"])*100).round(1)
    fig = px.imshow(
        wide.pivot(index=rows_col, columns=cols_col, values="delta_pct"),
        labels=dict(color="Δ pp (Rem−Hib)"),
        title=f"Heatmap de Delta por {rows_col} × {cols_col}"
    )
    return fig
