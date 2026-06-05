"""
dashboard.py — Tab 1: Executive Dashboard.

Menampilkan KPI makro, distribusi cluster, dan visualisasi PCA 2D/3D
untuk memberikan pandangan strategis tingkat tinggi.
"""

import pandas as pd
import streamlit as st

from config.settings import CLUSTER_PERSONAS
from src.visualizer import (
    create_cluster_bar,
    create_revenue_treemap,
    create_value_engagement_bubble,
    create_product_composition_bar,
)


def render(df: pd.DataFrame) -> None:
    """
    Merender konten Tab 1: Executive Dashboard.

    Args:
        df: DataFrame pelanggan lengkap dengan kolom 'Cluster'.
    """
    # --- Row 1: Macro KPIs ---
    st.markdown("### 📈 Key Performance Indicators")
    kpi_cols = st.columns(4)

    total_customers = len(df)
    dominant_cluster = int(df["Cluster"].mode().iloc[0])
    dominant_persona = CLUSTER_PERSONAS[dominant_cluster]

    avg_income = df["Income"].mean() if "Income" in df.columns else 0
    avg_spending = df["Total_Spent"].mean() if "Total_Spent" in df.columns else 0

    with kpi_cols[0]:
        st.metric(
            label="Total Pelanggan",
            value=f"{total_customers:,}",
            help="Jumlah total pelanggan dalam dataset",
        )
    with kpi_cols[1]:
        st.metric(
            label="Segmen Dominan",
            value=f"{dominant_persona['emoji']} C{dominant_cluster}",
            delta=dominant_persona["name"],
            delta_color="off",
            help="Cluster dengan jumlah pelanggan terbanyak",
        )
    with kpi_cols[2]:
        st.metric(
            label="Rata-rata Pendapatan",
            value=f"${avg_income:,.0f}",
            help="Pendapatan rata-rata seluruh pelanggan",
        )
    with kpi_cols[3]:
        st.metric(
            label="Rata-rata Pengeluaran",
            value=f"${avg_spending:,.0f}",
            help="Total pengeluaran rata-rata seluruh pelanggan",
        )

    st.divider()

    # --- Row 2: Customer Distribution and Revenue Contribution ---
    st.markdown("### 🎯 Ringkasan Segmen & Kontribusi Bisnis")
    dist_cols = st.columns(2)

    with dist_cols[0]:
        st.plotly_chart(create_cluster_bar(df), use_container_width=True)

    with dist_cols[1]:
        st.plotly_chart(create_revenue_treemap(df), use_container_width=True)

    st.divider()

    # --- Row 3: Segment Business Insights ---
    st.markdown("### 📊 Segment Business Insights")
    insight_cols = st.columns(2)

    with insight_cols[0]:
        st.plotly_chart(create_value_engagement_bubble(df), use_container_width=True)

    with insight_cols[1]:
        st.plotly_chart(create_product_composition_bar(df), use_container_width=True)

