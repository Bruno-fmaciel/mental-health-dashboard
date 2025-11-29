def insights_segments(df):
    if df is None or len(df) < 5 or "segment" not in df:
        return ["Dados insuficientes para gerar insights sobre segmentos."]

    insights = []

    # Estresse por segmento
    stress = df.groupby("segment")["stress_score"].mean().sort_values()
    insights.append(
        f"O segmento com maior estresse médio é **{stress.index[-1]}** (**{stress.iloc[-1]:.1f}**)."
    )

    # Burnout por segmento
    if "burnout_level" in df.columns:
        burn = (
            df["burnout_level"].eq("high")
            .groupby(df["segment"])
            .mean() * 100
        ).sort_values()

        insights.append(
            f"O maior burnout alto ocorre em **{burn.index[-1]}** (**{burn.iloc[-1]:.1f}%**)."
        )

    # Aviso de amostra pequena
    n_seg = df["segment"].value_counts()
    small = n_seg[n_seg < 15]
    if len(small) > 0:
        insights.append(
            f"Alguns segmentos têm **amostra reduzida** (ex.: {', '.join(small.index[:3])}), reduzindo a precisão da análise."
        )

    return insights
