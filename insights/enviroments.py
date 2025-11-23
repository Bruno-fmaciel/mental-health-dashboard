# insights/enviroments.py
def insights_enviroments(df, policy_col='policy'):
    insights = []
    if df is None or len(df) == 0 or policy_col not in df.columns:
        return ["Nenhum dado disponível para gerar insights sobre políticas."]

    # Risco alto por política (se burnout_level existir)
    if 'burnout_level' in df.columns:
        try:
            high_mask = df['burnout_level'] == 'high'
            pct_high = (high_mask.groupby(df[policy_col]).mean() * 100).dropna().sort_values()
            if len(pct_high) > 0:
                best = pct_high.index[0]
                worst = pct_high.index[-1]
                insights.append(f"A política **{best}** está associada ao menor burnout alto (**{pct_high.iloc[0]:.1f}%**).")
                insights.append(f"A política **{worst}** está associada ao maior burnout alto (**{pct_high.iloc[-1]:.1f}%**).")
        except Exception:
            pass

    # Tamanho das categorias
    try:
        counts = df[policy_col].value_counts(normalize=True) * 100
        if counts.iloc[0] > 70:
            insights.append(f"A categoria **{counts.index[0]}** representa >70% dos respondentes; resultados podem estar enviesados.")
    except Exception:
        pass

    return insights
