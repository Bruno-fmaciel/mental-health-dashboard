from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


# ---------- Helpers ----------
def _safe_mean(series: pd.Series) -> float:
    if series is None or series.dropna().empty:
        return float("nan")
    return float(series.dropna().mean())


def map_burnout_or_stress_to_numeric(series: pd.Series) -> pd.Series:
    if series is None:
        return series
    s = series.copy()

    if pd.api.types.is_numeric_dtype(s):
        return s.astype(float)

    map_low_med_high = {"Low": 2.0, "Medium": 5.0, "High": 8.0,
                        "low": 2.0, "medium": 5.0, "high": 8.0}
    map_no_maybe_yes = {"No": 0.0, "Maybe": 0.5, "Yes": 1.0,
                        "no": 0.0, "maybe": 0.5, "yes": 1.0}

    if s.dropna().astype(str).isin(map_low_med_high.keys()).any():
        return s.astype(str).map(map_low_med_high)
    if s.dropna().astype(str).isin(map_no_maybe_yes.keys()).any():
        return s.astype(str).map(map_no_maybe_yes)

    def try_num(x):
        try:
            return float(x)
        except Exception:
            return np.nan
    return s.apply(try_num)


# ---------- KPI cards ----------
def compute_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    n_resp = len(df)

    # detectar colunas compatíveis
    hours_col = next((c for c in df.columns if "Hour" in c or "Hours" in c), None)
    stress_col = next((c for c in df.columns if "Stress" in c), None)
    burnout_col = next((c for c in df.columns if "Burnout" in c), None)

    avg_hours = _safe_mean(df[hours_col]) if hours_col else float("nan")

    pct_high_stress = float("nan")
    if stress_col:
        stress_num = map_burnout_or_stress_to_numeric(df[stress_col])
        pct_high_stress = (stress_num >= 7).mean() * 100 if stress_num.max() > 1.5 else (stress_num >= 0.75).mean() * 100

    avg_burnout = float("nan")
    if burnout_col:
        bnum = map_burnout_or_stress_to_numeric(df[burnout_col])
        avg_burnout = _safe_mean(bnum)

    return {
        "n_resp": n_resp,
        "avg_hours": avg_hours,
        "pct_high_stress": pct_high_stress,
        "avg_burnout": avg_burnout,
        "hours_col": hours_col,
        "stress_col": stress_col,
        "burnout_col": burnout_col
    }


def kpi_cards(df: pd.DataFrame, title: Optional[str] = None):
    kpis = compute_kpis(df)

    if title:
        st.subheader(title)

    c1, c2, c3 = st.columns(3)
    c1.metric("Respondentes", f"{kpis['n_resp']:,}")
    c2.metric("Horas/Semana", f"{kpis['avg_hours']:.1f}" if not np.isnan(kpis['avg_hours']) else "N/A")
    c3.metric("% Estresse Alto", f"{kpis['pct_high_stress']:.1f}%" if not np.isnan(kpis['pct_high_stress']) else "N/A")


# ---------- Políticas Ambientais ----------
def stacked_env_policies(df: pd.DataFrame, title: Optional[str] = None, normalize: bool = True) -> px.bar:
    # identificar colunas mais prováveis
    policy_cols = [c for c in df.columns if "care" in c.lower() or "support" in c.lower() or "Access" in c or "Mental" in c]
    burnout_cols = [c for c in df.columns if "Burnout" in c or "Stress" in c]

    if not policy_cols:
        raise ValueError("Nenhuma coluna de política encontrada (care/support/mental).")
    if not burnout_cols:
        raise ValueError("Nenhuma coluna de burnout/stress encontrada.")

    policy = policy_cols[0]
    burnout = burnout_cols[0]

    tmp = df[[policy, burnout]].dropna()

    if pd.api.types.is_numeric_dtype(tmp[burnout]):
        tmp["_burnout_cat"] = pd.cut(tmp[burnout],
                                     bins=[-np.inf, tmp[burnout].quantile(0.33),
                                           tmp[burnout].quantile(0.66), np.inf],
                                     labels=["Low", "Medium", "High"])
        burnout = "_burnout_cat"

    title = title or f"{policy} vs {burnout}"

    df_ct = tmp.groupby([policy, burnout]).size().reset_index(name="count")
    df_tot = tmp.groupby(policy).size().reset_index(name="total")
    df_join = df_ct.merge(df_tot, on=policy)
    df_join["pct"] = df_join["count"] / df_join["total"]

    fig = px.bar(df_join, x=policy, y="pct", color=burnout, barmode="stack",
                 title=title,
                 labels={"pct": "Proporção", policy: "Política", burnout: "Burnout/Stress"})
    return fig


# ---------- Segmentos ----------
def small_multiples_segments(df: pd.DataFrame, top_n: int = 6, title: Optional[str] = None) -> px.bar:
    # identificar colunas de segmento (priorizar Industry, Region, Department, Occupation, Country)
    segment_col = next((c for c in df.columns if c in ["Industry", "Region", "Department", "Occupation", "Country"]), None)
    value_col = next((c for c in df.columns if "Burnout" in c or "Stress" in c or "Productivity" in c), None)

    if not segment_col:
        raise ValueError("Nenhum segmento encontrado.")
    if not value_col:
        raise ValueError("Nenhuma métrica (Burnout/Stress/Productivity) encontrada.")

    tmp = df[[segment_col, value_col]].dropna()
    if not pd.api.types.is_numeric_dtype(tmp[value_col]):
        tmp[value_col] = map_burnout_or_stress_to_numeric(tmp[value_col])

    agg_df = tmp.groupby(segment_col)[value_col].mean().reset_index().sort_values(value_col, ascending=False).head(top_n)
    title = title or f"Média de {value_col} por {segment_col}"

    fig = px.bar(agg_df, x=segment_col, y=value_col,
                 title=title,
                 labels={segment_col: "Segmento", value_col: "Média"},
                 text_auto=".2f")
    fig.update_layout(xaxis_tickangle=-30)
    return fig
