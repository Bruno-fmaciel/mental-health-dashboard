def insights_overview(df):
    insights = []

    if len(df) == 0:
        return ["Nenhum dado disponível para gerar insights."]

    # Stress
    if "stress_score" in df:
        mean_s = df["stress_score"].mean()
        insights.append(
            f"O nível médio de estresse é **{mean_s:.1f}**, indicando risco "
            f"{'alto' if mean_s>7 else 'moderado' if mean_s>4 else 'baixo'}."
        )

    # Burnout
    if "burnout_level" in df:
        high = (df["burnout_level"] == "high").mean() * 100
        insights.append(f"Burnout alto aparece em **{high:.1f}%** do grupo analisado.")

    # Horas
    if "hours_per_week" in df:
        hrs = df["hours_per_week"].mean()
        insights.append(
            f"A carga horária média é **{hrs:.1f}h**, "
            + ("acima do recomendado." if hrs > 40 else "dentro do esperado.")
        )

    return insights
