# insights/segments.py
def insights_segments(df):
    insights = []
    if df is None or len(df) == 0 or 'segment' not in df.columns:
        return ["Nenhum dado disponível para gerar insights sobre segmentos."]

    # Segmento com maior estresse médio
    try:
        stress = df.groupby("segment")["stress_score"].mean().dropna().sort_values()
        if len(stress) > 0:
            worst = stress.index[-1]
            insights.append(f"O segmento **{worst}** tem o maior estresse médio (**{stress.iloc[-1]:.1f}**).")
    except Exception:
        pass

    # Segmento com maior proporção de burnout alto (se disponível)
    if 'burnout_level' in df.columns:
        try:
            high = (df['burnout_level'] == 'high')
            pct = (high.groupby(df['segment']).mean() * 100).dropna().sort_values()
            if len(pct) > 0:
                worst_b = pct.index[-1]
                insights.append(f"O segmento com maior % de burnout alto é **{worst_b}** (**{pct.iloc[-1]:.1f}%**).")
        except Exception:
            pass

    # Amostra mínima por segmento (alerta)
    try:
        n_by_seg = df['segment'].value_counts()
        small = n_by_seg[n_by_seg < 15]
        if len(small) > 0:
            insights.append(f"Alguns segmentos têm pouca amostra (ex.: {', '.join(small.index[:3].astype(str))}); trate com cautela.")
    except Exception:
        pass

    return insights
