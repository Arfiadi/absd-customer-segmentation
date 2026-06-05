"""
profiling.py — Tab 2: Cluster Persona Profiling.

Menyediakan micro-analysis interaktif per cluster dengan:
- Deskripsi persona naratif
- Radar chart behavioral
- Breakdown pengeluaran
- Distribusi demografis
"""

import pandas as pd
import streamlit as st

from config.settings import CLUSTER_PERSONAS, SPENDING_COLS
from src.visualizer import (
    create_age_distribution,
    create_education_bar,
    create_income_boxplot,
    create_radar_chart,
    create_spending_breakdown,
    create_snake_plot,
    create_cluster_heatmap,
)


def _render_persona_card(cluster_id: int, df: pd.DataFrame) -> None:
    """
    Merender kartu informasi persona cluster.

    Menampilkan nama persona, deskripsi naratif, dan statistik
    ringkasan dalam format card yang informatif.

    Args:
        cluster_id: ID cluster (0-3).
        df: DataFrame pelanggan untuk menghitung statistik.
    """
    persona = CLUSTER_PERSONAS[cluster_id]
    cluster_data = df[df["Cluster"] == cluster_id]
    n_customers = len(cluster_data)
    pct = (n_customers / len(df)) * 100

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {persona['color']}22, {persona['color']}08);
            border-left: 4px solid {persona['color']};
            border-radius: 8px;
            padding: 20px 24px;
            margin-bottom: 16px;
        ">
            <h3 style="margin:0; color:{persona['color']};">
                {persona['emoji']} Cluster {cluster_id}: {persona['name']}
            </h3>
            <p style="margin:4px 0 0; color: #aaa; font-size: 0.9em;">
                {persona['subtitle']} &middot; {n_customers:,} pelanggan ({pct:.1f}%)
            </p>
            <p style="margin:12px 0 0; color: #ddd; line-height: 1.6;">
                {persona['description']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_key_stats(cluster_id: int, df: pd.DataFrame) -> None:
    """
    Merender statistik kunci cluster dalam bentuk metric cards.

    Args:
        cluster_id: ID cluster.
        df: DataFrame pelanggan.
    """
    cluster_data = df[df["Cluster"] == cluster_id]
    global_mean = df.select_dtypes(include="number").mean()
    cluster_mean = cluster_data.select_dtypes(include="number").mean()

    stat_cols = st.columns(4)
    stats = [
        ("Rata-rata Pendapatan", "Income", "${:,.0f}"),
        ("Rata-rata Pengeluaran", "Total_Spent", "${:,.0f}"),
        ("Rata-rata Usia", "Age", "{:.0f} thn"),
        ("Rata-rata Recency", "Recency", "{:.0f} hari"),
    ]

    for col, (label, feature, fmt) in zip(stat_cols, stats):
        if feature in cluster_mean.index:
            val = cluster_mean[feature]
            glob = global_mean[feature]
            delta = val - glob
            delta_str = fmt.format(abs(delta))
            if delta >= 0:
                delta_str = f"+{delta_str}"
            else:
                delta_str = f"-{delta_str}"

            with col:
                st.metric(
                    label=label,
                    value=fmt.format(val),
                    delta=f"{delta_str} vs global",
                )


def render(df: pd.DataFrame) -> None:
    """
    Merender konten Tab 2: Cluster Persona Profiling.

    Args:
        df: DataFrame pelanggan lengkap dengan kolom 'Cluster'.
    """
    st.markdown("### 🗺️ Perbandingan Makro Profil Cluster")
    
    col1, col2 = st.columns([7.5, 4.5])
    with col1:
        st.markdown("<h4 style='margin:0 0 10px 0; font-size:1.1em; color:#FAFAFA; font-weight:600;'>Snake Plot — Perbandingan Tren Relatif</h4>", unsafe_allow_html=True)
        st.plotly_chart(create_snake_plot(df), use_container_width=True)
    with col2:
        st.markdown("<h4 style='margin:0 0 10px 0; font-size:1.1em; color:#FAFAFA; font-weight:600;'>Heatmap Rata-rata Nilai Riil</h4>", unsafe_allow_html=True)
        st.plotly_chart(create_cluster_heatmap(df), use_container_width=True)

    st.divider()

    st.markdown("### 🔍 Pilih Cluster untuk Analisis Mendalam")

    # Interactive selector
    cluster_options = {
        f"{CLUSTER_PERSONAS[i]['emoji']} Cluster {i}: {CLUSTER_PERSONAS[i]['name']}": i
        for i in sorted(df["Cluster"].unique())
    }
    selected_label = st.radio(
        "Pilih Cluster",
        options=list(cluster_options.keys()),
        horizontal=True,
        label_visibility="collapsed",
    )
    selected_id = cluster_options[selected_label]

    st.divider()

    # --- Persona Card ---
    _render_persona_card(selected_id, df)

    # --- Key Stats ---
    _render_key_stats(selected_id, df)

    st.divider()

    # --- Row 1: Radar Chart + Spending Breakdown ---
    st.markdown("### 📊 Analisis Behavioral")
    chart_cols = st.columns(2)

    with chart_cols[0]:
        st.plotly_chart(
            create_radar_chart(df, selected_id),
            use_container_width=True,
        )

    with chart_cols[1]:
        st.plotly_chart(
            create_spending_breakdown(df, selected_id),
            use_container_width=True,
        )

    st.divider()

    # --- Row 2: Demographics ---
    st.markdown("### 👥 Analisis Demografis")
    demo_cols = st.columns(2)

    with demo_cols[0]:
        st.plotly_chart(
            create_age_distribution(df, selected_id),
            use_container_width=True,
        )

    with demo_cols[1]:
        st.plotly_chart(
            create_education_bar(df, selected_id),
            use_container_width=True,
        )

    # --- Income Boxplot (full width) ---
    st.plotly_chart(
        create_income_boxplot(df),
        use_container_width=True,
    )
