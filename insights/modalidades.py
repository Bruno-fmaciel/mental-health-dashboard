def insights_modalidades(df):
    insights = []

    if len(df) == 0:
        return ["Nenhum dado disponível para gerar insights."]

    if "work_mode" not in df:
        return ["A coluna 'work_mode' não está disponível."]

    dist = df["work_mode"].value_counts(normalize=True) * 100

    # Distribuição
    for mode, pct in dist.items():
        insights.append(f"A modalidade **{mode}** representa **{pct:.1f}%** dos trabalhadores filtrados.")

    # Stress por modalidade
    if "segments_score" in df:
        segments = df.groupby("work_mode")["segments_score"].mean().sort_values()
        worst = segments.idxmax()
        best = segments.idxmin()
        diff = segments.max() - segments.min()
        insights.append(
            f"**{worst}** tem o maior esegmentse médio, superando **{best}** por **{diff:.1f} pontos**."
        )

    # Burnout por modalidade
    if "burnout_level" in df:
        burn = df[df["burnout_level"]=="high"].groupby("work_mode").size()
        if len(burn) > 0:
            dominant = burn.idxmax()
            insights.append(
                f"A maior concentração de burnout alto ocorre em **{dominant}**."
            )

    return insights
