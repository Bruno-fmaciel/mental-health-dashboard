import pandas as pd

def insights_segments(df):
    if df is None or df.empty or len(df) < 5 or "segment" not in df.columns:
        return ["Dados insuficientes para gerar insights sobre segmentos."]

    insights = []

    # Estresse por segmento
    if "segment" in df.columns and "stress_score" in df.columns:
        stress = df.groupby("segment")["stress_score"].mean().sort_values()
        if len(stress) > 0:
            insights.append(
                f"O segmento com maior estresse médio é **{stress.index[-1]}** (**{stress.iloc[-1]:.1f}**) neste conjunto de dados."
            )

    # Burnout por segmento
    if "burnout_level" in df.columns and "segment" in df.columns:
        burn = (
            df["burnout_level"].eq("high")
            .groupby(df["segment"])
            .mean() * 100
        ).sort_values()

        if len(burn) > 0:
            insights.append(
                f"O maior burnout alto aparece em **{burn.index[-1]}** (**{burn.iloc[-1]:.1f}%**) neste conjunto de dados."
            )

    # Aviso de amostra pequena
    if "segment" in df.columns:
        n_seg = df["segment"].value_counts()
        small = n_seg[n_seg < 15]
        if len(small) > 0:
            insights.append(
                f"Alguns segmentos têm **amostra reduzida** (ex.: {', '.join(small.index[:3])}), o que pode afetar a precisão da análise."
            )

    return insights if insights else ["Dados insuficientes para gerar insights sobre segmentos."]
