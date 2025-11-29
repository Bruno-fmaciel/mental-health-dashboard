import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import textwrap

def kpi_cards(df_filtered, df_total):

    # ============================================
    # 1. Proteção contra DF vazio
    # ============================================
    if df_filtered.empty:
        st.info("Nenhum dado disponível para KPIs.")
        return

    # ============================================
    # 2. MÉTRICAS FILTRADAS
    # ============================================
    n = len(df_filtered)
    stress_mean = df_filtered["stress_score"].mean()
    burnout_high_pct = (df_filtered["burnout_level"] == "high").mean() * 100
    hours_mean = df_filtered["hours_per_week"].mean()

    # ============================================
    # 3. BENCHMARK GLOBAL
    # ============================================
    stress_global = df_total["stress_score"].mean()
    burnout_high_global = (df_total["burnout_level"] == "high").mean() * 100
    hours_global = df_total["hours_per_week"].mean()

    # ============================================
    # 4. DELTAS (com proteção contra NA)
    # ============================================
    def safe_delta(a, b):
        if a is None or b is None or b == 0:
            return 0
        return a - b

    delta_stress = safe_delta(stress_mean, stress_global)
    delta_burnout = safe_delta(burnout_high_pct, burnout_high_global)
    delta_hours = safe_delta(hours_mean, hours_global)

    # ============================================
    # FUNÇÃO DE COR DO DELTA
    # ============================================
    def color_delta(v, higher_is_bad=True):
        if np.isnan(v):
            return "#9ca3af"  # cinza
        if higher_is_bad:
            return "#ef4444" if v > 0 else "#10b981"
        else:
            return "#10b981" if v > 0 else "#ef4444"

    # ============================================
    # 5. LAYOUT EM 4 COLUNAS
    # ============================================
    col1, col2, col3, col4 = st.columns(4)

    # ============================================
    # TEMPLATE DE CARD PREMIUM
    # ============================================
    def render_card(col, value, label, delta, delta_label, color):
        html = f"""
        <div style="
            padding: 22px;
            border-radius: 14px;
            background: #1e293b;
            border: 1px solid #334155;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        ">
            <div style="font-size: 1.9rem; font-weight: 700; color:{color};">
                {value}
            </div>

            <div style="color:#e2e8f0; font-size: 1rem; margin-top:4px;">
                {label}
            </div>

            <div style="
                margin-top: 6px;
                font-size: 0.85rem;
                color: {color_delta(delta)};
            ">
                {delta_label}
            </div>
        </div>
        """
        col.html(textwrap.dedent(html))

    # ============================================
    # 6. RENDERIZA OS QUATRO KPIS
    # ============================================

    # --- RESPONDENTES ---
    render_card(
        col1,
        f"{n:,}",
        "Respondentes",
        0,  # respondentes não tem delta
        "Base filtrada",
        "#60a5fa"
    )

    # --- ESTRESSE ---
    render_card(
        col2,
        f"{stress_mean:.1f}",
        "Estresse Médio",
        delta_stress,
        f"Δ {delta_stress:+.2f} vs global",
        "#f87171"
    )

    # --- BURNOUT ALTO ---
    render_card(
        col3,
        f"{burnout_high_pct:.1f}%",
        "Burnout Alto",
        delta_burnout,
        f"Δ {delta_burnout:+.2f} pp vs global",
        "#fb7185"
    )

    # --- HORAS SEMANAIS ---
    render_card(
        col4,
        f"{hours_mean:.1f}h",
        "Horas por Semana",
        delta_hours,
        f"Δ {delta_hours:+.2f}h vs global",
        "#34d399"
    )


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


def stacked_env_policies(
    df: pd.DataFrame,
    policy_col: str = 'policy',
    min_pct: float = 5.0,
    show_percentages: bool = True
) -> go.Figure:
    """
    Cria gráfico de barras empilhadas mostrando a distribuição de burnout por política/condição.
    
    Args:
        df: DataFrame com os dados
        policy_col: Nome da coluna de política/condição a analisar
        min_pct: Percentual mínimo para não agrupar em "Outros" (default: 5%)
        show_percentages: Se True, mostra percentuais; se False, contagens absolutas
    
    Returns:
        Figura Plotly com barras empilhadas
    """
    if df is None or df.empty:
        return go.Figure()
    
    # Valida colunas necessárias
    if not set([policy_col, 'burnout_level']).issubset(df.columns):
        return go.Figure()
    
    # Copia e prepara dados
    df_work = df[[policy_col, 'burnout_level']].copy()
    df_work = df_work.dropna()
    
    if df_work.empty:
        return go.Figure()
    
    # Agrupa categorias raras em "Outros"
    counts = df_work[policy_col].value_counts(normalize=True) * 100
    rare_categories = counts[counts < min_pct].index.tolist()
    
    if rare_categories:
        df_work[policy_col] = df_work[policy_col].apply(
            lambda x: 'Outros' if x in rare_categories else x
        )
    
    # Agrupa por política e burnout
    ct = df_work.groupby([policy_col, 'burnout_level']).size().reset_index(name='n')
    
    if show_percentages:
        # Calcula % dentro de cada política
        ct['total_by_policy'] = ct.groupby(policy_col)['n'].transform('sum')
        ct['value'] = (ct['n'] / ct['total_by_policy'] * 100).round(1)
        y_label = "Percentual (%)"
    else:
        ct['value'] = ct['n']
        y_label = "Número de Respondentes"
    
    # Mapa de cores consistente
    color_map = {
        'low': '#4ECDC4',      # Verde/azul (baixo risco)
        'medium': '#FFE66D',   # Amarelo (risco médio)
        'high': '#FF6B6B'      # Vermelho (alto risco)
    }
    
    # Ordena burnout_level para garantir ordem consistente (low, medium, high)
    burnout_order = ['low', 'medium', 'high']
    ct['burnout_level'] = pd.Categorical(ct['burnout_level'], categories=burnout_order, ordered=True)
    ct = ct.sort_values(['burnout_level', policy_col])
    
    # Cria gráfico
    fig = px.bar(
        ct, 
        x=policy_col, 
        y='value', 
        color='burnout_level',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'burnout_level': burnout_order},
        labels={
            policy_col: 'Política/Condição',
            'value': y_label,
            'burnout_level': 'Nível de Burnout'
        }
    )
    
    # Adiciona texto nas barras
    fig.update_traces(
        texttemplate='%{y:.1f}' + ('%' if show_percentages else ''),
        textposition='inside',
        textfont_size=10
    )
    
    fig.update_layout(
        title="Distribuição de Burnout por Política de Suporte",
        xaxis_title="Política/Condição Organizacional",
        yaxis_title=y_label,
        legend_title="Nível de Burnout",
        hovermode='x unified',
        height=500
    )
    
    return fig


def compare_policies_risk(df: pd.DataFrame, policy_col: str = 'policy') -> pd.DataFrame:
    """
    Retorna tabela com análise de risco por política/condição.
    
    Args:
        df: DataFrame com os dados
        policy_col: Nome da coluna de política a analisar
    
    Returns:
        DataFrame com colunas: policy, n_total, pct_high, pct_medium, pct_low
        Ordenado por pct_high (decrescente)
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    if not set([policy_col, 'burnout_level']).issubset(df.columns):
        return pd.DataFrame()
    
    # Remove valores nulos
    df_work = df[[policy_col, 'burnout_level']].dropna()
    
    if df_work.empty:
        return pd.DataFrame()
    
    # Agrupa e calcula proporções
    grouped = df_work.groupby([policy_col, 'burnout_level']).size().unstack(fill_value=0)
    
    # Calcula percentuais
    totals = grouped.sum(axis=1)
    pct = (grouped.div(totals, axis=0) * 100).round(1)
    
    # Monta resultado
    result = pd.DataFrame({
        policy_col: pct.index,
        'n_total': totals.values
    })
    
    # Adiciona percentuais de cada nível
    for level in ['high', 'medium', 'low']:
        if level in pct.columns:
            result[f'pct_{level}'] = pct[level].values
        else:
            result[f'pct_{level}'] = 0.0
    
    # Ordena por risco alto (decrescente)
    result = result.sort_values('pct_high', ascending=False).reset_index(drop=True)
    
    return result


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
        title_text="Perfil de Risco: Compare Estresse, Burnout e Horas por Segmento",
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

def stress_distribution_premium(df):
    import plotly.graph_objects as go
    import numpy as np
    import plotly.express as px

    if df.empty:
        return go.Figure()

    x = df["stress_score"]

    fig = go.Figure()

    # HISTOGRAMA
    fig.add_trace(go.Histogram(
        x=x,
        nbinsx=20,
        marker=dict(
            color="#4A90E2",
            line=dict(color="#1e293b", width=1),
        ),
        opacity=0.65,
        name="Distribuição"
    ))

    # KDE (linha suave)
    kde_x = np.linspace(x.min(), x.max(), 200)
    kde_y = (
        (1 / (x.std() * np.sqrt(2 * np.pi))) *
        np.exp(-0.5 * ((kde_x - x.mean()) / x.std()) ** 2)
    )

    fig.add_trace(go.Scatter(
        x=kde_x,
        y=kde_y * len(x) * (x.max() - x.min()) / 20,
        mode="lines",
        line=dict(color="#f87171", width=3),
        name="Curva de Densidade"
    ))

    fig.update_layout(
        title="Distribuição de Estresse (Premium)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0f172a",
        font=dict(color="#e2e8f0"),
        bargap=0.05,
        margin=dict(l=15, r=15, t=40, b=15),
        height=380,
    )

    return fig

def hours_vs_stress_premium(df):
    import plotly.express as px
    import plotly.graph_objects as go

    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x="hours_per_week",
        y="stress_score",
        opacity=0.8,
        trendline="ols",
        color_discrete_sequence=["#60a5fa"],
        labels={
            "hours_per_week": "Horas por Semana",
            "stress_score": "Estresse"
        }
    )

    fig.update_traces(marker=dict(size=9, line=dict(width=1, color="#1e293b")))

    fig.update_layout(
        title="Carga Horária × Estresse (Premium)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0f172a",
        font=dict(color="#e2e8f0"),
        margin=dict(l=15, r=15, t=40, b=15),
        height=380,
    )

    return fig

def burnout_segments_premium(df):
    import plotly.express as px
    import plotly.graph_objects as go

    if df.empty or "segment" not in df.columns:
        return go.Figure()

    seg = df.groupby("segment")["burnout_level"].apply(
        lambda x: (x == "high").mean() * 100
    ).sort_values(ascending=True).tail(8)

    fig = px.bar(
        seg,
        orientation="h",
        labels={"value": "% Burnout Alto", "segment": "Segmento"},
        color=seg.values,
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        title="Top Segmentos com Maior Burnout (Premium)",
        coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0f172a",
        font=dict(color="#e2e8f0"),
        height=420,
        margin=dict(l=15, r=15, t=50, b=15),
    )

    return fig


def risk_heatmap_premium(df):
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go

    if df is None or df.empty:
        return go.Figure()

    df = df.copy()

    # Converte burnout para flag numérica
    if "burnout_level" in df.columns:
        df["burnout_flag"] = (df["burnout_level"] == "high").astype(int)

    # Seleciona SOMENTE colunas numéricas
    df_num = df.select_dtypes(include="number")

    # Se tiver menos de 2 variáveis, não há correlação possível
    if df_num.shape[1] < 2:
        fig = go.Figure()
        fig.add_annotation(
            text="Dados insuficientes para gerar o heatmap.",
            showarrow=False,
            font=dict(color="white", size=16)
        )
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)")
        return fig

    # Calcula correlação
    corr = df_num.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
        labels=dict(color="Correlação"),
        title="Mapa de Correlações entre Indicadores Numéricos (Premium)"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0f172a",
        font=dict(color="#e2e8f0"),
        margin=dict(l=40, r=40, t=70, b=40),
        height=450,
    )

    return fig


