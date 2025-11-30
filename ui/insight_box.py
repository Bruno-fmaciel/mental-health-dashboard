import streamlit as st
import re
import textwrap

def _convert_markdown_bold_to_html(text: str) -> str:
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

def insight_box(title: str, insights: list[str]):
    """
    Card premium de insights automáticos.
    Renderiza HTML puro usando st.html (não markdown).
    """

    if not insights:
        insights = ["Nenhum insight disponível para os filtros atuais."]

    # Converte **markdown** para <strong>
    items_html = "".join(
        f"<li style='margin-bottom:6px;'>{_convert_markdown_bold_to_html(i)}</li>"
        for i in insights
    )

    html = textwrap.dedent(f"""
    <div style="
        padding:22px; border-radius:14px;
        background:linear-gradient(135deg, #2A2A2A 0%, #1A1A1A 100%);
        border:1px solid #444;
        box-shadow:0 2px 8px rgba(0,0,0,0.45);
        margin-top:25px; margin-bottom:25px;
        ">

        <div style="display:flex; align-items:center; gap:12px;">
            <div style="font-size:34px;">🤖</div>
            <div>
                <h3 style="margin:0; color:#F1F1F1;">{title}</h3>
                <p style="margin:0; font-size:15px; color:#BBBBBB;">
                    Baseado nos filtros ativos desta página.
                </p>
            </div>
        </div>

        <hr style="margin-top:16px; border:0; border-top:1px solid #555;"/>

        <ul style="font-size:16px; color:#EDEDED; margin-left:10px; padding-left:10px;">
            {items_html}
        </ul>

    </div>
    """)

    # 👇 ESSA É A LINHA QUE RESOLVE TUDO
    st.html(html)