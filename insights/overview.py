import pandas as pd

def insights_overview(df):
    if df is None or df.empty or len(df) < 5:
        return ["Dados insuficientes para gerar insights na visão geral."]

    insights = []

    # ESTRESSE
    if "stress_score" in df.columns:
        mean_s = df["stress_score"].mean()
        if not pd.isna(mean_s):
            risk = "alto" if mean_s >= 6 else "moderado" if mean_s >= 4 else "baixo"
            insights.append(
                f"O estresse médio está em **{mean_s:.1f}**, indicando risco **{risk}** para o grupo analisado."
            )

    # BURNOUT
    if "burnout_level" in df.columns:
        pct_high = (df["burnout_level"] == "high").mean() * 100
        if not pd.isna(pct_high):
            insights.append(
                f"O burnout alto aparece em **{pct_high:.1f}%** das pessoas filtradas, um indicador relevante para monitoramento."
            )

    # HORAS
    if "hours_per_week" in df.columns:
        avg_h = df["hours_per_week"].mean()
        if not pd.isna(avg_h):
            nivel = 'acima' if avg_h > 40 else 'dentro'
            insights.append(
                f"A carga média de trabalho está em **{avg_h:.1f}h/semana**, nível {nivel} do recomendado."
            )

    return insights if insights else ["Dados insuficientes para gerar insights na visão geral."]
