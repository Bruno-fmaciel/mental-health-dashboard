"""
Utilitários para o Dashboard de Saúde Mental.
"""

from .data_io import load_data, render_sidebar
from .charts import (
    # Overview functions
    make_overview_kpi_cards,
    plot_stress_distribution_histogram,
    plot_burnout_level_composition,
    plot_core_correlation_heatmap,
    # Burnout functions
    make_burnout_kpi_cards,
    plot_hours_vs_stress_scatter,
    plot_stress_by_hours_band,
    plot_roles_burnout_ranking,
    # Environment functions
    make_environment_kpi_cards,
    plot_burnout_distribution_by_policy,
    plot_policy_burnout_ranking,
    make_policy_summary_table,
    # Work mode functions
    make_workmode_kpi_cards,
    plot_stress_by_workmode,
    plot_burnout_by_workmode,
    plot_workmode_delta_heatmap,
    # Segments functions
    make_segments_kpi_cards,
    plot_segment_burnout_ranking,
    plot_segment_stress_mean,
    make_segment_summary_table,
    # Legacy functions (for backward compatibility)
    kpi_cards,
    scatter_hours_burnout,
    box_burnout_by_role,
    stacked_env_policies,
    violin_by_workmode,
    plot_delta_heatmap,
)

__all__ = [
    'load_data',
    'render_sidebar',
    # Overview
    'make_overview_kpi_cards',
    'plot_stress_distribution_histogram',
    'plot_burnout_level_composition',
    'plot_core_correlation_heatmap',
    # Burnout
    'make_burnout_kpi_cards',
    'plot_hours_vs_stress_scatter',
    'plot_stress_by_hours_band',
    'plot_roles_burnout_ranking',
    # Environment
    'make_environment_kpi_cards',
    'plot_burnout_distribution_by_policy',
    'plot_policy_burnout_ranking',
    'make_policy_summary_table',
    # Work mode
    'make_workmode_kpi_cards',
    'plot_stress_by_workmode',
    'plot_burnout_by_workmode',
    'plot_workmode_delta_heatmap',
    # Segments
    'make_segments_kpi_cards',
    'plot_segment_burnout_ranking',
    'plot_segment_stress_mean',
    'make_segment_summary_table',
    # Legacy
    'kpi_cards',
    'scatter_hours_burnout',
    'box_burnout_by_role',
    'stacked_env_policies',
    'violin_by_workmode',
    'plot_delta_heatmap',
]
