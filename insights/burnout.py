def insights_burnout(df):
    insights = []

    if len(df) == 0:
        return ["Nenhum dado disponível para gerar insights."]

    high_pct = (df["burnout_level"] == "high").mean() * 100
    insights.append(f"Burnout alto aparece em **{high_pct:.1f}%** dos trabalhadores filtrados.")

    if "hours_per_week" in df:
        high_hours = df[df["hours_per_week"] > 50]
        pct_high = (high_hours["burnout_level"]=="high").mean() * 100
        insights.append(f"Entre aqueles com mais de 50h semanais, burnout alto sobe para **{pct_high:.1f}%**.")

    if "stress_score" in df:
        corr = df["stress_score"].corr(df["burnout_level"].eq("high").astype(int))
        if corr > 0.3:
            insights.append("Burnout alto está fortemente associado a níveis elevados de estresse.")

    return insights
