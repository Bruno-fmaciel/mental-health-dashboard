def insights_enviroments(df, policy_col="policy"):
    if df is None or len(df) < 5 or policy_col not in df:
        return ["Dados insuficientes para gerar insights sobre políticas."]

    insights = []

    # Burnout por política
    if "burnout_level" in df.columns:
        grouped = (
            df["burnout_level"].eq("high")
            .groupby(df[policy_col])
            .mean() * 100
        ).sort_values()

        if len(grouped) > 1:
            best = grouped.index[0]
            worst = grouped.index[-1]
            insights.append(
                f"A política **{best}** apresenta o **menor burnout** (**{grouped.iloc[0]:.1f}%**), enquanto **{worst}** tem o **maior risco** (**{grouped.iloc[-1]:.1f}%**)."
            )

    # Se uma política domina os dados (>70%)
    dist = df[policy_col].value_counts(normalize=True) * 100
    if dist.iloc[0] > 70:
        insights.append(
            f"A categoria **{dist.index[0]}** domina os dados (**{dist.iloc[0]:.1f}%**), o que pode enviesar interpretações."
        )

    return insights
