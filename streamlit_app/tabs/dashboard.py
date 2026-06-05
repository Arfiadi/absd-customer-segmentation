"""
dashboard.py — Tab 1: Executive Dashboard.

Menampilkan KPI makro, distribusi cluster, dan visualisasi PCA 2D/3D
untuk memberikan pandangan strategis tingkat tinggi.
"""

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.decomposition import PCA

from config.settings import CLUSTER_PERSONAS, FEATURES_B, SPENDING_COLS
from src.inference import load_models
from src.visualizer import (
    create_cluster_bar,
    create_cluster_donut,
    create_pca_scatter_2d,
    create_pca_scatter_3d,
)


def _compute_pca_components(df: pd.DataFrame) -> dict:
    """
    Menghitung komponen PCA dari data historis untuk visualisasi.

    Melakukan scaling + PCA transform pada seluruh data pelanggan
    untuk menghasilkan koordinat scatter plot.

    Args:
        df: DataFrame dengan kolom FEATURES_B dan 'Cluster'.

    Returns:
        Dict dengan key 'pc1', 'pc2', dan opsional 'pc3'.
    """
    scaler, pca_model, _ = load_models()

    # Prepare 28-feature input for scaler
    from config.settings import ALL_SCALER_FEATURES
    full_input = pd.DataFrame(0, index=df.index, columns=ALL_SCALER_FEATURES)
    for col in FEATURES_B:
        if col in df.columns:
            full_input[col] = df[col].values

    scaled = pd.DataFrame(
        scaler.transform(full_input),
        columns=ALL_SCALER_FEATURES,
        index=df.index,
    )
    scaled_21 = scaled[FEATURES_B]

    # 2D PCA (menggunakan model champion)
    pca_2d = pca_model.transform(scaled_21)

    # 3D PCA (fit baru dengan 3 komponen untuk visualisasi)
    pca_3d_model = PCA(n_components=3, random_state=42)
    pca_3d = pca_3d_model.fit_transform(scaled_21)

    return {
        "pc1": pca_2d[:, 0],
        "pc2": pca_2d[:, 1],
        "pc1_3d": pca_3d[:, 0],
        "pc2_3d": pca_3d[:, 1],
        "pc3_3d": pca_3d[:, 2],
    }


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

    # --- Row 2: Cluster Distribution ---
    st.markdown("### 🎯 Distribusi Cluster")
    dist_cols = st.columns(2)

    with dist_cols[0]:
        st.plotly_chart(create_cluster_donut(df), width="stretch")
    with dist_cols[1]:
        st.plotly_chart(create_cluster_bar(df), width="stretch")

    st.divider()

    # --- Row 3: PCA Scatter Plots ---
    st.markdown("### 🔬 Visualisasi PCA — Separasi Cluster")

    with st.spinner("Menghitung komponen PCA..."):
        pca_data = _compute_pca_components(df)

    pca_cols = st.columns([1, 1])

    with pca_cols[0]:
        st.plotly_chart(
            create_pca_scatter_2d(df, pca_data["pc1"], pca_data["pc2"]),
            width="stretch",
        )

    with pca_cols[1]:
        st.plotly_chart(
            create_pca_scatter_3d(
                df, pca_data["pc1_3d"], pca_data["pc2_3d"], pca_data["pc3_3d"]
            ),
            width="stretch",
        )
