import pandas as pd

def insights_burnout(df):
    if df is None or df.empty or len(df) < 5:
        return ["Dados insuficientes para gerar insights sobre burnout."]

    insights = []

    if "burnout_level" in df.columns:
        high_pct = (df["burnout_level"] == "high").mean() * 100
        insights.append(
            f"O burnout alto atinge **{high_pct:.1f}%** do grupo atual."
        )

    # Carga horária > 50h
    if "hours_per_week" in df.columns and "burnout_level" in df.columns:
        over = df[df["hours_per_week"] > 50]
        if len(over) >= 5:
            pct = (over["burnout_level"] == "high").mean() * 100
            insights.append(
                f"Entre trabalhadores com mais de 50h semanais, o burnout alto aparece em **{pct:.1f}%** deste grupo."
            )

    # Correlação estresse × burnout
    if "stress_score" in df.columns and "burnout_level" in df.columns:
        corr = df["stress_score"].corr(df["burnout_level"].eq("high").astype(int))
        if not pd.isna(corr) and corr > 0.25:
            insights.append(
                f"Há uma **correlação positiva ({corr:.2f})** entre estresse e burnout neste conjunto de dados, indicando associação entre essas variáveis."
            )

    return insights if insights else ["Dados insuficientes para gerar insights sobre burnout."]
