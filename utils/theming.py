"""
Módulo para configuração de temas e estilos do dashboard.
"""
import streamlit as st


def set_page_theme():
    """
    Aplica CSS customizado para melhorar a aparência do dashboard.
    Mantém alinhado com .streamlit/config.toml; aqui você pode centralizar estilos globais.
    """
    st.markdown("""
    <style>
        /* Estilo para cards de métricas */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 600;
        }
        
        /* Estilo para títulos */
        h1 {
            color: #4A90E2;
            padding-bottom: 1rem;
        }
        
        h2 {
            color: #2C3E50;
            padding-top: 1rem;
        }
        
        /* Estilo para dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 8px;
        }
        
        /* Estilo para botões */
        .stButton>button {
            border-radius: 8px;
            background-color: #4A90E2;
            color: white;
            border: none;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #357ABD;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Estilo para sidebar */
        [data-testid="stSidebar"] {
            background-color: #F8F9FA;
        }
        
        /* Estilo para tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
        }
        
        /* Classe pequena para texto secundário */
        .small {
            font-size: 0.85rem;
            color: var(--text-color-secondary);
        }
    </style>
    """, unsafe_allow_html=True)


def add_footer():
    """
    Adiciona um rodapé personalizado ao dashboard.
    """
    st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">
    <div style="text-align: center; color: #7F8C8D; font-size: 0.9rem;">
        <p>Dashboard de Saúde Mental no Trabalho | SR2 - Projetos 5</p>
        <p>Desenvolvido com ❤️ usando Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

