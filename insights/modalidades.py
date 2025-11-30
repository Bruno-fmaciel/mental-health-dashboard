import pandas as pd

def insights_modalidades(df):
    if df is None or df.empty or len(df) < 5 or "work_mode" not in df.columns:
        return ["Dados insuficientes para gerar insights sobre modalidades."]

    insights = []

    if "work_mode" in df.columns:
        dist = df["work_mode"].value_counts(normalize=True) * 100
        for mode, pct in dist.items():
            insights.append(f"A modalidade **{mode}** representa **{pct:.1f}%** do grupo analisado.")

    # Burnout por modalidade
    if "burnout_level" in df.columns and "work_mode" in df.columns:
        pct_burn = (
            df[df["burnout_level"] == "high"].groupby("work_mode").size()
            / df.groupby("work_mode").size()
            * 100
        ).dropna()

        if len(pct_burn) > 0:
            worst = pct_burn.idxmax()
            insights.append(
                f"A maior taxa de burnout alto aparece em **{worst}** (**{pct_burn.max():.1f}%**) neste conjunto de dados."
            )

    return insights if insights else ["Dados insuficientes para gerar insights sobre modalidades."]
