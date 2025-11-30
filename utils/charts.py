"""
Chart functions using Plotly Express for the mental health dashboard.
All functions return Plotly Figure objects for use with st.plotly_chart().
"""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import textwrap

# ============================================================================
# COLOR SEMANTICS: Higher risk → red-ish, Lower risk → green-ish
# ============================================================================
COLOR_HIGH_RISK = '#FF6B6B'  # Red
COLOR_MEDIUM_RISK = '#FFE66D'  # Yellow
COLOR_LOW_RISK = '#4ECDC4'  # Green/Teal
COLOR_NEUTRAL = '#60a5fa'  # Blue

BURNOUT_COLOR_MAP = {
    'high': COLOR_HIGH_RISK,
    'medium': COLOR_MEDIUM_RISK,
    'low': COLOR_LOW_RISK
}


# ============================================================================
# OVERVIEW PAGE FUNCTIONS (1_Visao_Geral.py)
# ============================================================================

def make_overview_kpi_cards(df):
    """Returns 4 KPIs: number of respondents, average stress score, % high burnout, average hours per week."""
    if df.empty:
        return None, None, None, None
    
    n = len(df)
    stress_mean = df["stress_score"].mean() if "stress_score" in df.columns else 0
    burnout_high_pct = (df["burnout_level"] == "high").mean() * 100 if "burnout_level" in df.columns else 0
    hours_mean = df["hours_per_week"].mean() if "hours_per_week" in df.columns else 0
    
    return n, stress_mean, burnout_high_pct, hours_mean


def plot_stress_distribution_histogram(df):
    """Uses px.histogram with x=stress_score, appropriate bins, optional marginal."""
    if df.empty or 'stress_score' not in df.columns:
        return go.Figure()
    
    fig = px.histogram(
        df,
        x='stress_score',
        nbins=20,
        marginal='box',
        title="Distribuição de estresse",
        labels={'stress_score': 'Score de Estresse', 'count': 'Frequência'},
        color_discrete_sequence=[COLOR_NEUTRAL]
    )
    fig.update_layout(
        xaxis_title="Score de Estresse",
        yaxis_title="Número de Respondentes",
        showlegend=False
    )
    return fig


def plot_burnout_level_composition(df):
    """Uses px.bar or px.pie/donut to show proportion of burnout levels."""
    if df.empty or 'burnout_level' not in df.columns:
        return go.Figure()
    
    burnout_counts = df['burnout_level'].value_counts()
    burnout_df = pd.DataFrame({
        'burnout_level': burnout_counts.index,
        'count': burnout_counts.values
    })
    
    # Use pie chart for composition
    fig = px.pie(
        burnout_df,
        values='count',
        names='burnout_level',
        title="Níveis de burnout",
        color='burnout_level',
        color_discrete_map=BURNOUT_COLOR_MAP,
        category_orders={'burnout_level': ['low', 'medium', 'high']}
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def plot_core_correlation_heatmap(df):
    """Compute correlation matrix for numeric variables and use px.imshow."""
    if df.empty:
        return go.Figure()
    
    # Select only numeric columns relevant for correlation
    numeric_cols = []
    if 'stress_score' in df.columns:
        numeric_cols.append('stress_score')
    if 'hours_per_week' in df.columns:
        numeric_cols.append('hours_per_week')
    
    # Add burnout_numeric if available, or create it
    if 'burnout_level' in df.columns:
        df = df.copy()
        df['burnout_numeric'] = df['burnout_level'].map({'low': 1, 'medium': 2, 'high': 3}).fillna(2)
        numeric_cols.append('burnout_numeric')
    
    if len(numeric_cols) < 2:
        return go.Figure()
    
    corr_df = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        aspect='auto',
        title="Correlação entre variáveis-chave",
        labels=dict(color="Correlação")
    )
    fig.update_layout(
        xaxis_title="",
        yaxis_title=""
    )
    return fig


# ============================================================================
# BURNOUT PAGE FUNCTIONS (pages/2_Burnout.py)
# ============================================================================

def make_burnout_kpi_cards(df):
    """Returns KPIs: % high burnout, average stress_score, average hours_per_week."""
    if df.empty:
        return None, None, None
    
    burnout_high_pct = (df["burnout_level"] == "high").mean() * 100 if "burnout_level" in df.columns else 0
    stress_mean = df["stress_score"].mean() if "stress_score" in df.columns else 0
    hours_mean = df["hours_per_week"].mean() if "hours_per_week" in df.columns else 0
    
    return burnout_high_pct, stress_mean, hours_mean


def plot_hours_vs_stress_scatter(df):
    """Uses px.scatter with x=hours_per_week, y=stress_score, trendline='ols', optional color by work_mode."""
    if df.empty or not all(col in df.columns for col in ['hours_per_week', 'stress_score']):
        return go.Figure()
    
    color_col = 'work_mode' if 'work_mode' in df.columns else None
    
    fig = px.scatter(
        df,
        x='hours_per_week',
        y='stress_score',
        color=color_col,
        trendline='ols',
        title="Horas de trabalho × Estresse",
        labels={
            'hours_per_week': 'Horas por Semana',
            'stress_score': 'Score de Estresse'
        }
    )
    fig.update_layout(
        xaxis_title="Horas por Semana",
        yaxis_title="Score de Estresse"
    )
    return fig


def plot_stress_by_hours_band(df):
    """Uses px.violin or px.box with x=hours_band, y=stress_score."""
    if df.empty or 'hours_per_week' not in df.columns or 'stress_score' not in df.columns:
        return go.Figure()
    
    df = df.copy()
    # Create hours_band if not exists
    if 'hours_band' not in df.columns:
        df['hours_band'] = pd.cut(
            df['hours_per_week'],
            bins=[0, 35, 45, 100],
            labels=['<35h', '35–45h', '>45h']
        )
    
    fig = px.violin(
        df,
        x='hours_band',
        y='stress_score',
        box=True,
        points='all',
        title="Estresse por faixa de horas",
        labels={
            'hours_band': 'Faixa de Horas',
            'stress_score': 'Score de Estresse'
        },
        color_discrete_sequence=[COLOR_NEUTRAL]
    )
    fig.update_layout(
        xaxis_title="Faixa de Horas",
        yaxis_title="Score de Estresse"
    )
    return fig


def plot_roles_burnout_ranking(df):
    """Aggregate by role, compute % high burnout, use px.bar horizontal sorted descending."""
    if df.empty or 'role' not in df.columns or 'burnout_level' not in df.columns:
        return go.Figure()
    
    # Calculate high burnout rate per role
    role_stats = df.groupby('role').agg({
        'burnout_level': lambda x: (x == 'high').mean() * 100,
        'role': 'count'
    }).rename(columns={'burnout_level': 'high_burnout_rate', 'role': 'n'})
    
    # Filter out roles with tiny N (less than 5)
    role_stats = role_stats[role_stats['n'] >= 5]
    
    if role_stats.empty:
        return go.Figure()
    
    role_stats = role_stats.sort_values('high_burnout_rate', ascending=True).reset_index()
    
    fig = px.bar(
        role_stats,
        x='high_burnout_rate',
        y='role',
        orientation='h',
        title="Cargos com maior risco de burnout",
        labels={
            'high_burnout_rate': '% Burnout Alto',
            'role': 'Cargo'
        },
        color='high_burnout_rate',
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        xaxis_title="% Burnout Alto",
        yaxis_title="Cargo",
        coloraxis_showscale=False
    )
    return fig


# ============================================================================
# ENVIRONMENT PAGE FUNCTIONS (pages/3_Ambiente_Trabalho.py)
# ============================================================================

def make_environment_kpi_cards(df):
    """Returns KPIs: number of distinct policies, overall % high burnout, overall average stress_score."""
    if df.empty:
        return None, None, None
    
    n_policies = df['policy'].nunique() if 'policy' in df.columns else 0
    burnout_high_pct = (df["burnout_level"] == "high").mean() * 100 if "burnout_level" in df.columns else 0
    stress_mean = df["stress_score"].mean() if "stress_score" in df.columns else 0
    
    return n_policies, burnout_high_pct, stress_mean


def plot_burnout_distribution_by_policy(df):
    """For each policy, compute proportion of burnout levels. Use px.bar with barmode='stack'."""
    if df.empty or 'policy' not in df.columns or 'burnout_level' not in df.columns:
        return go.Figure()
    
    # Group by policy and burnout_level
    policy_burnout = df.groupby(['policy', 'burnout_level']).size().reset_index(name='count')
    policy_totals = df.groupby('policy').size().reset_index(name='total')
    policy_burnout = policy_burnout.merge(policy_totals, on='policy')
    policy_burnout['proportion'] = (policy_burnout['count'] / policy_burnout['total'] * 100).round(1)
    
    # Filter policies with minimum sample size
    policy_burnout = policy_burnout[policy_burnout['total'] >= 5]
    
    if policy_burnout.empty:
        return go.Figure()
    
    fig = px.bar(
        policy_burnout,
        x='policy',
        y='proportion',
        color='burnout_level',
        barmode='stack',
        title="Distribuição de burnout por política",
        labels={
            'policy': 'Política',
            'proportion': '% de Respondentes',
            'burnout_level': 'Nível de Burnout'
        },
        color_discrete_map=BURNOUT_COLOR_MAP,
        category_orders={'burnout_level': ['low', 'medium', 'high']}
    )
    fig.update_layout(
        xaxis_title="Política",
        yaxis_title="% de Respondentes"
    )
    return fig


def plot_policy_burnout_ranking(df):
    """Aggregate by policy, compute high_burnout_rate, use px.bar horizontal sorted descending."""
    if df.empty or 'policy' not in df.columns or 'burnout_level' not in df.columns:
        return go.Figure()
    
    policy_stats = df.groupby('policy').agg({
        'burnout_level': lambda x: (x == 'high').mean() * 100,
        'policy': 'count'
    }).rename(columns={'burnout_level': 'high_burnout_rate', 'policy': 'n'})
    
    # Filter out policies with tiny N
    policy_stats = policy_stats[policy_stats['n'] >= 5]
    
    if policy_stats.empty:
        return go.Figure()
    
    policy_stats = policy_stats.sort_values('high_burnout_rate', ascending=True).reset_index()
    
    fig = px.bar(
        policy_stats,
        x='high_burnout_rate',
        y='policy',
        orientation='h',
        title="Políticas com maior % de burnout alto",
        labels={
            'high_burnout_rate': '% Burnout Alto',
            'policy': 'Política'
        },
        color='high_burnout_rate',
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        xaxis_title="% Burnout Alto",
        yaxis_title="Política",
        coloraxis_showscale=False
    )
    return fig


def make_policy_summary_table(df):
    """Returns summary dataframe: [policy_name, N, average_stress, high_burnout_rate]."""
    if df.empty or 'policy' not in df.columns:
        return pd.DataFrame()
    
    summary = df.groupby('policy').agg({
        'policy': 'count',
        'stress_score': 'mean',
        'burnout_level': lambda x: (x == 'high').mean() * 100
    }).rename(columns={
        'policy': 'N',
        'stress_score': 'average_stress',
        'burnout_level': 'high_burnout_rate'
    }).reset_index()
    
    summary.columns = ['policy_name', 'N', 'average_stress', 'high_burnout_rate']
    summary = summary.sort_values('high_burnout_rate', ascending=False)
    
    return summary


# ============================================================================
# WORK MODES PAGE FUNCTIONS (pages/4_Remoto_Hibrido.py)
# ============================================================================

def make_workmode_kpi_cards(df):
    """Summarize per work_mode (remote, hybrid, onsite). Returns ordered dict."""
    if df.empty or 'work_mode' not in df.columns:
        return {}
    
    workmode_stats = df.groupby('work_mode').agg({
        'burnout_level': lambda x: (x == 'high').mean() * 100,
        'stress_score': 'mean',
        'hours_per_week': 'mean',
        'work_mode': 'count'
    }).rename(columns={
        'burnout_level': 'high_burnout_pct',
        'stress_score': 'avg_stress',
        'hours_per_week': 'avg_hours',
        'work_mode': 'n'
    })
    
    # Order: onsite → hybrid → remote
    ordered_modes = ['onsite', 'hybrid', 'remote']
    result = {}
    for mode in ordered_modes:
        if mode in workmode_stats.index:
            result[mode] = workmode_stats.loc[mode].to_dict()
    
    # Add any remaining modes not in the standard order
    for mode in workmode_stats.index:
        if mode not in result:
            result[mode] = workmode_stats.loc[mode].to_dict()
    
    return result


def plot_stress_by_workmode(df):
    """Uses px.violin or px.box with x=work_mode, y=stress_score."""
    if df.empty or 'work_mode' not in df.columns or 'stress_score' not in df.columns:
        return go.Figure()
    
    # Order: onsite → hybrid → remote
    workmode_order = ['onsite', 'hybrid', 'remote']
    
    fig = px.violin(
        df,
        x='work_mode',
        y='stress_score',
        box=True,
        points='all',
        title="Estresse por modalidade de trabalho",
        labels={
            'work_mode': 'Modalidade',
            'stress_score': 'Score de Estresse'
        },
        color='work_mode',
        color_discrete_sequence=[COLOR_NEUTRAL, '#4ECDC4', '#FFE66D'],
        category_orders={'work_mode': workmode_order}
    )
    fig.update_layout(
        xaxis_title="Modalidade de Trabalho",
        yaxis_title="Score de Estresse",
        showlegend=False
    )
    return fig


def plot_burnout_by_workmode(df):
    """Aggregate by work_mode, compute high_burnout_rate, use px.bar."""
    if df.empty or 'work_mode' not in df.columns or 'burnout_level' not in df.columns:
        return go.Figure()
    
    workmode_stats = df.groupby('work_mode').agg({
        'burnout_level': lambda x: (x == 'high').mean() * 100
    }).rename(columns={'burnout_level': 'high_burnout_rate'}).reset_index()
    
    # Order: onsite → hybrid → remote (only include modes that exist in data)
    workmode_order = ['onsite', 'hybrid', 'remote']
    available_modes = [m for m in workmode_order if m in workmode_stats['work_mode'].values]
    if available_modes:
        workmode_stats['work_mode'] = pd.Categorical(
            workmode_stats['work_mode'],
            categories=available_modes,
            ordered=True
        )
        workmode_stats = workmode_stats.sort_values('work_mode')
    
    fig = px.bar(
        workmode_stats,
        x='work_mode',
        y='high_burnout_rate',
        title="Burnout alto por modalidade",
        labels={
            'work_mode': 'Modalidade',
            'high_burnout_rate': '% Burnout Alto'
        },
        color='high_burnout_rate',
        color_continuous_scale='Reds',
        category_orders={'work_mode': workmode_order}
    )
    fig.update_layout(
        xaxis_title="Modalidade de Trabalho",
        yaxis_title="% Burnout Alto",
        coloraxis_showscale=False
    )
    return fig


def plot_workmode_delta_heatmap(df, segment_dim, delta_type):
    """
    Compute deltas in high_burnout_rate between work modes for each segment.
    delta_type: 'Remoto − Híbrido', 'Remoto − Presencial', 'Híbrido − Presencial'
    Uses px.imshow to show deltas as a simple bar chart (since we only have one dimension).
    """
    if df.empty or segment_dim not in df.columns or 'work_mode' not in df.columns or 'burnout_level' not in df.columns:
        return go.Figure()
    
    # Parse delta_type - handle both em dash and regular dash
    if ' − ' in delta_type:
        modes = delta_type.split(' − ')
    elif ' - ' in delta_type:
        modes = delta_type.split(' - ')
    else:
        return go.Figure()
    
    if len(modes) != 2:
        return go.Figure()
    
    # Map Portuguese names to lowercase work_mode values
    mode_map = {
        'remoto': 'remote',
        'híbrido': 'hybrid',
        'presencial': 'onsite'
    }
    
    mode1 = mode_map.get(modes[0].lower().strip(), modes[0].lower().strip())
    mode2 = mode_map.get(modes[1].lower().strip(), modes[1].lower().strip())
    
    # Normalize work_mode to lowercase for comparison
    df = df.copy()
    df['work_mode_lower'] = df['work_mode'].str.lower().str.strip()
    
    # Filter to only the two modes we're comparing
    df_filtered = df[df['work_mode_lower'].isin([mode1, mode2])]
    
    if df_filtered.empty:
        return go.Figure()
    
    # Calculate high burnout rate per segment and work mode
    segment_mode_stats = df_filtered.groupby([segment_dim, 'work_mode_lower']).agg({
        'burnout_level': lambda x: (x == 'high').mean() * 100,
        segment_dim: 'count'
    }).rename(columns={segment_dim: 'n'}).reset_index()
    
    # Filter segments with minimum sample size
    segment_mode_stats = segment_mode_stats[segment_mode_stats['n'] >= 5]
    
    if segment_mode_stats.empty:
        return go.Figure()
    
    # Pivot to get rates for each mode
    pivot_df = segment_mode_stats.pivot(index=segment_dim, columns='work_mode_lower', values='burnout_level')
    
    # Calculate delta
    if mode1 in pivot_df.columns and mode2 in pivot_df.columns:
        pivot_df['delta'] = pivot_df[mode1] - pivot_df[mode2]
        pivot_df = pivot_df.reset_index()
        
        # Sort by delta descending
        pivot_df = pivot_df.sort_values('delta', ascending=False)
        
        # Create horizontal bar chart showing deltas
        # Create clearer label
        mode1_label = modes[0].strip()
        mode2_label = modes[1].strip()
        xaxis_label = f"Diferença em p.p. de burnout alto ({mode1_label} − {mode2_label})"
        
        fig = px.bar(
            pivot_df,
            x='delta',
            y=segment_dim,
            orientation='h',
            title=f"Delta de burnout entre modalidades por segmento",
            labels={
                'delta': xaxis_label,
                segment_dim: 'Segmento'
            },
            color='delta',
            color_continuous_scale='RdBu_r',
            color_continuous_midpoint=0
        )
        fig.update_layout(
            xaxis_title=xaxis_label,
            yaxis_title="Segmento",
            coloraxis_showscale=True,
            coloraxis_colorbar=dict(
                title="Δ p.p."
            )
        )
        return fig
    
    return go.Figure()


# ============================================================================
# SEGMENTS PAGE FUNCTIONS (pages/5_Perfis_Segmentos.py)
# ============================================================================

def make_segments_kpi_cards(df, segmentation):
    """Returns KPIs: number of segments, % in critical segments, overall high_burnout_rate."""
    if df.empty or segmentation not in df.columns:
        return None, None, None
    
    n_segments = df[segmentation].nunique()
    
    # Calculate high burnout rate per segment
    segment_stats = df.groupby(segmentation).agg({
        'burnout_level': lambda x: (x == 'high').mean() * 100
    }).reset_index()
    segment_stats = segment_stats.sort_values('burnout_level', ascending=False)
    
    # Top 3 critical segments
    top3 = segment_stats.head(3)
    if not top3.empty:
        top3_total = df[df[segmentation].isin(top3[segmentation])].shape[0]
        pct_critical = (top3_total / len(df)) * 100 if len(df) > 0 else 0
    else:
        pct_critical = 0
    
    overall_high_burnout = (df['burnout_level'] == 'high').mean() * 100 if 'burnout_level' in df.columns else 0
    
    return n_segments, pct_critical, overall_high_burnout


def plot_segment_burnout_ranking(df, segmentation):
    """Aggregate by segmentation, compute high_burnout_rate, use px.bar horizontal sorted descending."""
    if df.empty or segmentation not in df.columns or 'burnout_level' not in df.columns:
        return go.Figure()
    
    segment_stats = df.groupby(segmentation).agg({
        'burnout_level': lambda x: (x == 'high').mean() * 100,
        segmentation: 'count'
    }).rename(columns={'burnout_level': 'high_burnout_rate', segmentation: 'n'})
    
    # Filter out segments with tiny N
    segment_stats = segment_stats[segment_stats['n'] >= 5]
    
    if segment_stats.empty:
        return go.Figure()
    
    segment_stats = segment_stats.sort_values('high_burnout_rate', ascending=True).reset_index()
    
    # Adjust height based on number of segments (min 300, max 600, ~50px per segment)
    n_segments = len(segment_stats)
    height = max(300, min(600, 50 + (n_segments * 50)))
    
    fig = px.bar(
        segment_stats,
        x='high_burnout_rate',
        y=segmentation,
        orientation='h',
        title="Segmentos com maior % de burnout alto",
        labels={
            'high_burnout_rate': '% Burnout Alto',
            segmentation: 'Segmento'
        },
        color='high_burnout_rate',
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        xaxis_title="% Burnout Alto",
        yaxis_title="Segmento",
        coloraxis_showscale=False,
        height=height
    )
    return fig


def plot_segment_stress_mean(df, segmentation):
    """Similar aggregation but for average stress_score. px.bar horizontal."""
    if df.empty or segmentation not in df.columns or 'stress_score' not in df.columns:
        return go.Figure()
    
    segment_stats = df.groupby(segmentation).agg({
        'stress_score': 'mean',
        segmentation: 'count'
    }).rename(columns={'stress_score': 'stress_mean', segmentation: 'n'})
    
    # Filter out segments with tiny N
    segment_stats = segment_stats[segment_stats['n'] >= 5]
    
    if segment_stats.empty:
        return go.Figure()
    
    segment_stats = segment_stats.sort_values('stress_mean', ascending=True).reset_index()
    
    # Adjust height based on number of segments (min 300, max 600, ~50px per segment)
    n_segments = len(segment_stats)
    height = max(300, min(600, 50 + (n_segments * 50)))
    
    fig = px.bar(
        segment_stats,
        x='stress_mean',
        y=segmentation,
        orientation='h',
        title="Estresse médio por segmento",
        labels={
            'stress_mean': 'Estresse Médio',
            segmentation: 'Segmento'
        },
        color='stress_mean',
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        xaxis_title="Estresse Médio",
        yaxis_title="Segmento",
        coloraxis_showscale=False,
        height=height
    )
    return fig


def make_segment_summary_table(df, segmentation):
    """Returns summary dataframe: [segment, N, stress_mean, hours_mean, high_burnout_rate]."""
    if df.empty or segmentation not in df.columns:
        return pd.DataFrame()
    
    summary = df.groupby(segmentation).agg({
        segmentation: 'count',
        'stress_score': 'mean',
        'hours_per_week': 'mean',
        'burnout_level': lambda x: (x == 'high').mean() * 100
    }).rename(columns={
        segmentation: 'N',
        'stress_score': 'stress_mean',
        'hours_per_week': 'hours_mean',
        'burnout_level': 'high_burnout_rate'
    }).reset_index()
    
    summary.columns = ['segment', 'N', 'stress_mean', 'hours_mean', 'high_burnout_rate']
    summary = summary.sort_values('high_burnout_rate', ascending=False)
    
    return summary


# ============================================================================
# LEGACY FUNCTIONS (kept for backward compatibility)
# ============================================================================

def kpi_cards(df_filtered, df_total):
    """Legacy KPI cards function - kept for backward compatibility."""
    if df_filtered.empty:
        st.info("Nenhum dado disponível para KPIs.")
        return
    
    n = len(df_filtered)
    stress_mean = df_filtered["stress_score"].mean()
    burnout_high_pct = (df_filtered["burnout_level"] == "high").mean() * 100
    hours_mean = df_filtered["hours_per_week"].mean()
    
    stress_global = df_total["stress_score"].mean()
    burnout_high_global = (df_total["burnout_level"] == "high").mean() * 100
    hours_global = df_total["hours_per_week"].mean()
    
    def safe_delta(a, b):
        if a is None or b is None or b == 0:
            return 0
        return a - b
    
    delta_stress = safe_delta(stress_mean, stress_global)
    delta_burnout = safe_delta(burnout_high_pct, burnout_high_global)
    delta_hours = safe_delta(hours_mean, hours_global)
    
    def color_delta(v, higher_is_bad=True):
        if np.isnan(v):
            return "#9ca3af"
        if higher_is_bad:
            return "#ef4444" if v > 0 else "#10b981"
        else:
            return "#10b981" if v > 0 else "#ef4444"
    
    col1, col2, col3, col4 = st.columns(4)
    
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
    
    render_card(col1, f"{n:,}", "Respondentes", 0, "Base filtrada", "#60a5fa")
    render_card(col2, f"{stress_mean:.1f}", "Estresse Médio", delta_stress, f"Δ {delta_stress:+.2f} vs global", "#f87171")
    render_card(col3, f"{burnout_high_pct:.1f}%", "Burnout Alto", delta_burnout, f"Δ {delta_burnout:+.2f} pp vs global", "#fb7185")
    render_card(col4, f"{hours_mean:.1f}h", "Horas por Semana", delta_hours, f"Δ {delta_hours:+.2f}h vs global", "#34d399")


def scatter_hours_burnout(df):
    """Legacy function - use plot_hours_vs_stress_scatter instead."""
    return plot_hours_vs_stress_scatter(df)


def box_burnout_by_role(df):
    """Legacy function - kept for backward compatibility."""
    if df.empty or 'role' not in df.columns or 'stress_score' not in df.columns:
        return go.Figure()
    fig = px.box(df, x='role', y='stress_score', points='all')
    fig.update_layout(title="Estresse por Cargo/Modalidade", xaxis_title="Cargo", yaxis_title="Estresse")
    return fig


def stacked_env_policies(df, policy_col='policy', min_pct=5.0, show_percentages=True):
    """Legacy function - use plot_burnout_distribution_by_policy instead."""
    return plot_burnout_distribution_by_policy(df)


def compare_policies_risk(df, policy_col='policy'):
    """Legacy function - use make_policy_summary_table instead."""
    return make_policy_summary_table(df)


def violin_by_workmode(df):
    """Legacy function - use plot_stress_by_workmode instead."""
    return plot_stress_by_workmode(df)


def plot_delta_heatmap(df, rows_col, cols_col, mode_col="work_mode", **kwargs):
    """Legacy function - simplified version."""
    # This is a simplified version - the new plot_workmode_delta_heatmap is more focused
    if df.empty or rows_col not in df.columns or cols_col not in df.columns:
        return go.Figure()
    
    # For now, use a simple approach
    df = df[df[mode_col].isin(["Remote", "Hybrid"])].copy()
    df["_risk_flag"] = (
        (df.get("burnout_level", "").astype(str).str.lower() == "high")
    )
    
    g = df.groupby([rows_col, cols_col, mode_col]).agg(
        risk=("_risk_flag", "mean"), n=("_risk_flag", "size")
    ).reset_index()
    
    wide = g.pivot_table(index=[rows_col, cols_col], columns=mode_col, values="risk").reset_index()
    for m in ["Remote", "Hybrid"]:
        if m not in wide.columns:
            wide[m] = np.nan
    
    wide["delta_pct"] = ((wide["Remote"] - wide["Hybrid"]) * 100).round(1)
    fig = px.imshow(
        wide.pivot(index=rows_col, columns=cols_col, values="delta_pct"),
        labels=dict(color="Δ pp (Rem−Hib)"),
        title=f"Heatmap de Delta por {rows_col} × {cols_col}"
    )
    return fig
