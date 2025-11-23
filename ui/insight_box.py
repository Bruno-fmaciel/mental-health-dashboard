import streamlit as st

def insight_box(title: str = "Insights Automáticos", content: str = ""):
    html = f"""
<div style="padding:22px; border-radius:14px;
background:linear-gradient(135deg, #2A2A2A 0%, #1A1A1A 100%);
border:1px solid #444; box-shadow:0 2px 8px rgba(0,0,0,0.45);
margin-top:25px; margin-bottom:25px;">

<div style="display:flex; align-items:center; gap:12px;">
    <div style="font-size:34px;">🤖</div>
    <div>
        <h3 style="margin:0; padding:0; color:#F1F1F1;">{title}</h3>
        <p style="margin:0; font-size:15px; color:#BBBBBB;">
            Gerados automaticamente com base nos filtros ativos do dashboard.
        </p>
    </div>
</div>

<hr style="margin-top:16px; border:0; border-top:1px solid #555;"/>

<div style="font-size:16px; color:#EDEDED;">
    {content}
</div>

</div>
"""
    st.markdown(html, unsafe_allow_html=True)
