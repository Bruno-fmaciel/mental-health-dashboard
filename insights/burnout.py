def insights_burnout(df):
    if df is None or len(df) < 5:
        return ["Dados insuficientes para gerar insights sobre burnout."]

    insights = []

    high_pct = (df["burnout_level"] == "high").mean() * 100
    insights.append(
        f"O burnout alto atinge **{high_pct:.1f}%** do grupo atual."
    )

    # Carga horária > 50h
    if "hours_per_week" in df.columns:
        over = df[df["hours_per_week"] > 50]
        if len(over) >= 5:
            pct = (over["burnout_level"] == "high").mean() * 100
            insights.append(
                f"Entre trabalhadores com mais de 50h semanais, o burnout alto sobe para **{pct:.1f}%**."
            )

    # Correlação estresse × burnout
    if "stress_score" in df.columns:
        corr = df["stress_score"].corr(df["burnout_level"].eq("high").astype(int))
        if corr > 0.25:
            insights.append(
                f"Há uma **correlação positiva ({corr:.2f})** entre estresse e burnout, reforçando a relação entre sobrecarga e esgotamento."
            )

    return insights
