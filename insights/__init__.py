"""
Módulo de geração automática de insights para as páginas do dashboard.
"""
from .overview import insights_overview
from .modalidades import insights_modalidades
from .burnout import insights_burnout
from .segments import insights_segments
from .enviroments import insights_enviroments

__all__ = [
    "insights_overview",
    "insights_modalidades",
    "insights_burnout",
    "insights_segments",
    "insights_enviroments",
]