"""
visualizer.py — Mesin visualisasi interaktif berbasis Plotly.

Menyediakan fungsi-fungsi pembantu untuk membuat chart yang konsisten
secara visual di seluruh tab aplikasi.
"""

from typing import List, Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.settings import (
    CLUSTER_COLORS,
    CLUSTER_PERSONAS,
    FEATURES_B,
    PURCHASE_CHANNEL_COLS,
    SPENDING_COLS,
)

# ---------------------------------------------------------------------------
# Shared Layout Defaults
# ---------------------------------------------------------------------------
_LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#FAFAFA"),
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(
        bgcolor="rgba(26,31,46,0.8)",
        bordercolor="rgba(108,99,255,0.3)",
        borderwidth=1,
    ),
)


def _apply_defaults(fig: go.Figure, **overrides) -> go.Figure:
    """Menerapkan layout default pada figure Plotly."""
    layout = {**_LAYOUT_DEFAULTS, **overrides}
    fig.update_layout(**layout)
    return fig


# ---------------------------------------------------------------------------
# Dashboard Charts
# ---------------------------------------------------------------------------
def create_cluster_bar(df: pd.DataFrame) -> go.Figure:
    """
    Membuat bar chart distribusi cluster dengan statistik persentase.

    Args:
        df: DataFrame dengan kolom 'Cluster'.

    Returns:
        Figure Plotly bar chart.
    """
    counts = df["Cluster"].value_counts().sort_index()
    total = len(df)
    names = [f"C{i}" for i in counts.index]
    percentages = (counts / total * 100).round(1)
    
    custom_names = [CLUSTER_PERSONAS[i]['name'] for i in counts.index]
    custom_data = np.stack((custom_names, percentages), axis=-1)
    
    colors = [CLUSTER_COLORS[i] for i in counts.index]
    max_count = counts.max()

    fig = go.Figure(
        data=[
            go.Bar(
                x=names,
                y=counts.values,
                customdata=custom_data,
                marker=dict(
                    color=colors,
                    line=dict(color="rgba(255,255,255,0.2)", width=1),
                ),
                text=[f"{val:,} users ({pct}%)" for val, pct in zip(counts.values, percentages)],
                textposition="outside",
                textfont=dict(size=14, color="#FAFAFA"),
                hovertemplate="<b>%{x}: %{customdata[0]}</b><br>Jumlah: %{y} (%{customdata[1]}%)<extra></extra>",
            )
        ]
    )
    _apply_defaults(
        fig,
        title="Distribusi Populasi Pelanggan per Cluster",
        xaxis=dict(title="Cluster"),
        yaxis=dict(
            title="Jumlah Pelanggan",
            gridcolor="rgba(255,255,255,0.1)",
            range=[0, max_count * 1.15],
        ),
        height=420,
        margin=dict(l=50, r=40, t=80, b=60),
    )
    return fig


def create_snake_plot(df: pd.DataFrame) -> go.Figure:
    """
    Membuat Snake Plot (Line Chart) perbandingan mean fitur kontinu antar cluster.

    Args:
        df: DataFrame pelanggan.

    Returns:
        Figure Plotly line chart (Snake Plot).
    """
    # Kolom kontinu kunci (18 fitur numerik penting dari FEATURES_B)
    continuous_features = [
        # Demographics
        "Age", "Income", "Customer_Tenure", "Kidhome", "Teenhome",
        # Spending
        "MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds",
        # Channels
        "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases",
        # Engagement/Behavior
        "NumWebVisitsMonth", "Recency", "Total_Promos", "NumDealsPurchases"
    ]
    available_features = [f for f in continuous_features if f in df.columns]

    if not available_features:
        return go.Figure()

    # Hitung rata-rata per cluster
    cluster_means = df.groupby("Cluster")[available_features].mean()

    # Normalisasi Min-Max (0-1) agar fitur dalam skala yang sama (Y-axis)
    min_vals = cluster_means.min()
    max_vals = cluster_means.max()
    range_vals = max_vals - min_vals
    range_vals = range_vals.replace(0, 1) # Hindari division by zero

    normalized_means = (cluster_means - min_vals) / range_vals

    # Reset index dan unpivot data untuk Plotly Express
    normalized_means = normalized_means.reset_index()
    melted_df = normalized_means.melt(id_vars="Cluster", var_name="Feature", value_name="Normalized Value")

    # Mapping Persona untuk warna dan legend
    melted_df["Persona"] = melted_df["Cluster"].apply(lambda x: f"C{x}: {CLUSTER_PERSONAS[x]['name']}")

    fig = px.line(
        melted_df,
        x="Feature",
        y="Normalized Value",
        color="Persona",
        color_discrete_map={f"C{i}: {CLUSTER_PERSONAS[i]['name']}": CLUSTER_PERSONAS[i]["color"] for i in CLUSTER_PERSONAS},
        markers=True,
    )
    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Skor Relatif: %{y:.2f}<extra></extra>",
        line=dict(width=3),
        marker=dict(size=8)
    )

    _apply_defaults(
        fig,
        title="Snake Plot — Perbandingan Makro Profil Cluster",
        xaxis=dict(title="", tickangle=-45, gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(title="Skor Normalisasi (0-1)", gridcolor="rgba(255,255,255,0.1)", range=[-0.05, 1.15]),
        height=500,
        margin=dict(l=50, r=40, t=80, b=120),
    )
    
    return fig


def create_cluster_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Membuat Heatmap Rata-rata Fitur per Cluster dengan Row Normalization.
    Menampilkan visualisasi densitas/peringkat per fitur secara relatif
    sekaligus menampilkan angka rata-rata sebenarnya pada tabel.

    Args:
        df: DataFrame pelanggan.

    Returns:
        Figure Plotly heatmap.
    """
    continuous_features = [
        # Demographics
        "Age", "Income", "Customer_Tenure", "Kidhome", "Teenhome",
        # Spending
        "MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds",
        # Channels
        "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases",
        # Engagement/Behavior
        "NumWebVisitsMonth", "Recency", "Total_Promos", "NumDealsPurchases"
    ]
    available_features = [f for f in continuous_features if f in df.columns]

    if not available_features:
        return go.Figure()

    # Hitung rata-rata per cluster
    cluster_means = df.groupby("Cluster")[available_features].mean()

    # Transpose agar Fitur di Y-axis (baris) dan Cluster di X-axis (kolom)
    df_heat = cluster_means.T

    # Normalisasi per baris (fitur) agar bisa dibandingkan walau beda skala
    row_min = df_heat.min(axis=1)
    row_max = df_heat.max(axis=1)
    row_range = row_max - row_min
    row_range = row_range.replace(0, 1) # Hindari division by zero
    df_heat_norm = df_heat.sub(row_min, axis=0).div(row_range, axis=0)

    # Label untuk Cluster (menggunakan short name agar tabel kompak)
    cluster_names = [f"C{i}" for i in df_heat.columns]

    # Format angka rata-rata untuk anotasi tabel
    def format_val(feature: str, val: float) -> str:
        if "Income" in feature:
            return f"${val/1000:.1f}k" if val >= 1000 else f"${val:.0f}"
        elif "Spent" in feature or feature.startswith("Mnt"):
            return f"${val:.0f}"
        elif "Tenure" in feature:
            return f"{val:.0f}d"
        elif "Age" in feature:
            return f"{val:.1f}"
        elif "Purchases" in feature or "Visits" in feature or "Deals" in feature:
            return f"{val:.1f}x"
        elif "Promos" in feature or "home" in feature:
            return f"{val:.2f}"
        elif "Recency" in feature:
            return f"{val:.1f}d"
        else:
            return f"{val:.1f}"

    # Buat custom data untuk hover template dan teks anotasi
    custom_text = []
    annotations = []
    
    for y_idx, feature in enumerate(df_heat.index):
        row_text = []
        for x_idx, cluster in enumerate(df_heat.columns):
            raw_val = df_heat.loc[feature, cluster]
            norm_val = df_heat_norm.loc[feature, cluster]
            text_val = format_val(feature, raw_val)
            row_text.append(text_val)
            
            # Tentukan warna teks (kontras)
            text_color = "#111111" if norm_val > 0.6 else "#FAFAFA"
            
            annotations.append(
                dict(
                    x=x_idx,
                    y=y_idx,
                    text=text_val,
                    showarrow=False,
                    font=dict(color=text_color, size=11, family="Inter, sans-serif"),
                )
            )
        custom_text.append(row_text)

    # Custom colorscale: dari Navy Slate gelap (background dashboard) ke Purple brand ke Teal brand
    custom_colorscale = [
        [0.0, "#1A1F2E"],
        [0.5, "#6C63FF"],
        [1.0, "#4ECDC4"]
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=df_heat_norm.values,
            x=cluster_names,
            y=df_heat.index,
            customdata=custom_text,
            colorscale=custom_colorscale,
            showscale=False, # Sembunyikan colorbar karena normalisasi per baris
            xgap=2,
            ygap=2,
            hovertemplate="<b>%{y} (Cluster %{x})</b><br>Rata-rata: %{customdata}<br>Skor Relatif: %{z:.2f}<extra></extra>"
        )
    )

    _apply_defaults(
        fig,
        title="Heatmap Nilai Rata-rata Fitur per Cluster",
        xaxis=dict(title="Cluster", side="bottom"),
        yaxis=dict(title="", gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11)),
        height=500,
        margin=dict(l=140, r=40, t=80, b=120),
        annotations=annotations
    )

    return fig


def create_pca_scatter_2d(df: pd.DataFrame, pc1: np.ndarray, pc2: np.ndarray) -> go.Figure:
    """
    Membuat scatter plot PCA 2D interaktif.

    Args:
        df: DataFrame dengan kolom 'Cluster'.
        pc1: Array nilai Principal Component 1.
        pc2: Array nilai Principal Component 2.

    Returns:
        Figure Plotly scatter 2D.
    """
    plot_df = pd.DataFrame({"PC1": pc1, "PC2": pc2, "Cluster": df["Cluster"].values})

    fig = go.Figure()
    for cluster_id in sorted(plot_df["Cluster"].unique()):
        mask = plot_df["Cluster"] == cluster_id
        persona = CLUSTER_PERSONAS[cluster_id]
        fig.add_trace(
            go.Scatter(
                x=plot_df.loc[mask, "PC1"],
                y=plot_df.loc[mask, "PC2"],
                mode="markers",
                name=f"{persona['emoji']} C{cluster_id}: {persona['name']}",
                marker=dict(
                    color=persona["color"],
                    size=6,
                    opacity=0.7,
                    line=dict(width=0.5, color="rgba(255,255,255,0.3)"),
                ),
                hovertemplate=(
                    f"<b>{persona['name']}</b><br>"
                    "PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra></extra>"
                ),
            )
        )

    _apply_defaults(
        fig,
        title="PCA 2D — Separasi Cluster",
        xaxis=dict(title="Principal Component 1", gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(title="Principal Component 2", gridcolor="rgba(255,255,255,0.08)"),
        height=500,
    )
    return fig


def create_pca_scatter_3d(
    df: pd.DataFrame, pc1: np.ndarray, pc2: np.ndarray, pc3: np.ndarray
) -> go.Figure:
    """
    Membuat scatter plot PCA 3D interaktif.

    Args:
        df: DataFrame dengan kolom 'Cluster'.
        pc1, pc2, pc3: Array nilai komponen PCA.

    Returns:
        Figure Plotly scatter 3D.
    """
    plot_df = pd.DataFrame({
        "PC1": pc1, "PC2": pc2, "PC3": pc3, "Cluster": df["Cluster"].values,
    })

    fig = go.Figure()
    for cluster_id in sorted(plot_df["Cluster"].unique()):
        mask = plot_df["Cluster"] == cluster_id
        persona = CLUSTER_PERSONAS[cluster_id]
        fig.add_trace(
            go.Scatter3d(
                x=plot_df.loc[mask, "PC1"],
                y=plot_df.loc[mask, "PC2"],
                z=plot_df.loc[mask, "PC3"],
                mode="markers",
                name=f"{persona['emoji']} C{cluster_id}",
                marker=dict(color=persona["color"], size=3, opacity=0.7),
            )
        )

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="PC1", backgroundcolor="rgba(0,0,0,0)"),
            yaxis=dict(title="PC2", backgroundcolor="rgba(0,0,0,0)"),
            zaxis=dict(title="PC3", backgroundcolor="rgba(0,0,0,0)"),
        ),
        **_LAYOUT_DEFAULTS,
        title="PCA 3D — Separasi Cluster",
        height=550,
    )
    return fig


# ---------------------------------------------------------------------------
# Profiling Charts
# ---------------------------------------------------------------------------
def create_radar_chart(
    df: pd.DataFrame,
    cluster_id: int,
    features: Optional[List[str]] = None,
) -> go.Figure:
    """
    Membuat Radar Chart perbandingan profil cluster vs global mean.

    Args:
        df: DataFrame dengan kolom fitur dan 'Cluster'.
        cluster_id: ID cluster yang akan dianalisis.
        features: Daftar fitur untuk radar (default: fitur behavioral).

    Returns:
        Figure Plotly radar chart.
    """
    if features is None:
        features = SPENDING_COLS + PURCHASE_CHANNEL_COLS + ["NumWebVisitsMonth", "Recency"]

    available = [f for f in features if f in df.columns]
    if not available:
        return go.Figure()

    # Normalisasi min-max agar semua fitur sebanding di radar
    global_mean = df[available].mean()
    cluster_mean = df[df["Cluster"] == cluster_id][available].mean()

    # Normalisasi ke 0-1 berdasarkan range data
    min_vals = df[available].min()
    max_vals = df[available].max()
    range_vals = max_vals - min_vals
    range_vals = range_vals.replace(0, 1)  # Hindari division by zero

    global_norm = ((global_mean - min_vals) / range_vals).values
    cluster_norm = ((cluster_mean - min_vals) / range_vals).values

    persona = CLUSTER_PERSONAS[cluster_id]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=np.append(global_norm, global_norm[0]),
            theta=available + [available[0]],
            fill="toself",
            name="Rata-rata Global",
            line=dict(color="rgba(255,255,255,0.5)", dash="dot"),
            fillcolor="rgba(255,255,255,0.05)",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=np.append(cluster_norm, cluster_norm[0]),
            theta=available + [available[0]],
            fill="toself",
            name=f"C{cluster_id}: {persona['name']}",
            line=dict(color=persona["color"], width=2),
            fillcolor=f"rgba({_hex_to_rgb(persona['color'])},0.15)",
        )
    )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(size=9),
            ),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        ),
        **_LAYOUT_DEFAULTS,
        title=f"Profil Behavioral — {persona['emoji']} {persona['name']}",
        height=480,
    )
    return fig


def create_spending_breakdown(df: pd.DataFrame, cluster_id: int) -> go.Figure:
    """
    Membuat grouped bar chart pengeluaran per kategori produk.

    Membandingkan rata-rata cluster vs rata-rata global.

    Args:
        df: DataFrame dengan kolom SPENDING_COLS dan 'Cluster'.
        cluster_id: ID cluster yang akan dianalisis.

    Returns:
        Figure Plotly grouped bar chart.
    """
    available = [c for c in SPENDING_COLS if c in df.columns]
    if not available:
        return go.Figure()

    global_mean = df[available].mean()
    cluster_mean = df[df["Cluster"] == cluster_id][available].mean()
    persona = CLUSTER_PERSONAS[cluster_id]
    max_val = max(global_mean.max(), cluster_mean.max()) if len(available) > 0 else 0

    # Clean labels
    labels = [c.replace("Mnt", "").replace("Products", "").replace("Prods", "") for c in available]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=global_mean.values,
            name="Rata-rata Global",
            marker_color="rgba(255,255,255,0.3)",
            text=[f"${v:.0f}" for v in global_mean.values],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            x=labels,
            y=cluster_mean.values,
            name=f"C{cluster_id}: {persona['name']}",
            marker_color=persona["color"],
            text=[f"${v:.0f}" for v in cluster_mean.values],
            textposition="outside",
        )
    )

    _apply_defaults(
        fig,
        title=f"Pengeluaran per Kategori — {persona['emoji']} {persona['name']}",
        barmode="group",
        xaxis=dict(title="Kategori Produk"),
        yaxis=dict(
            title="Rata-rata Pengeluaran ($)",
            gridcolor="rgba(255,255,255,0.1)",
            range=[0, max_val * 1.15] if max_val > 0 else None,
        ),
        height=420,
    )
    return fig


def create_age_distribution(df: pd.DataFrame, cluster_id: int) -> go.Figure:
    """
    Membuat histogram distribusi umur untuk cluster tertentu vs global.

    Args:
        df: DataFrame dengan kolom 'Age' dan 'Cluster'.
        cluster_id: ID cluster yang akan dianalisis.

    Returns:
        Figure Plotly histogram.
    """
    persona = CLUSTER_PERSONAS[cluster_id]
    cluster_data = df[df["Cluster"] == cluster_id]

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=df["Age"],
            name="Semua Pelanggan",
            marker_color="rgba(255,255,255,0.2)",
            opacity=0.5,
            nbinsx=20,
        )
    )
    fig.add_trace(
        go.Histogram(
            x=cluster_data["Age"],
            name=f"C{cluster_id}: {persona['name']}",
            marker_color=persona["color"],
            opacity=0.7,
            nbinsx=20,
        )
    )

    _apply_defaults(
        fig,
        title=f"Distribusi Usia — {persona['emoji']} {persona['name']}",
        barmode="overlay",
        xaxis=dict(title="Usia (Tahun)"),
        yaxis=dict(title="Jumlah Pelanggan", gridcolor="rgba(255,255,255,0.1)"),
        height=380,
    )
    return fig


def create_income_boxplot(df: pd.DataFrame) -> go.Figure:
    """
    Membuat box plot distribusi pendapatan per cluster.

    Args:
        df: DataFrame dengan kolom 'Income' dan 'Cluster'.

    Returns:
        Figure Plotly box plot.
    """
    fig = go.Figure()
    for cluster_id in sorted(df["Cluster"].unique()):
        persona = CLUSTER_PERSONAS[cluster_id]
        cluster_data = df[df["Cluster"] == cluster_id]
        fig.add_trace(
            go.Box(
                y=cluster_data["Income"],
                name=f"C{cluster_id}: {persona['name']}",
                marker_color=persona["color"],
                boxmean=True,
            )
        )

    _apply_defaults(
        fig,
        title="Distribusi Pendapatan per Cluster",
        yaxis=dict(title="Pendapatan ($)", gridcolor="rgba(255,255,255,0.1)"),
        height=420,
    )
    return fig


def create_education_bar(df: pd.DataFrame, cluster_id: int) -> go.Figure:
    """
    Membuat bar chart distribusi tingkat pendidikan dalam cluster.

    Args:
        df: DataFrame dengan kolom 'Education' dan 'Cluster'.
        cluster_id: ID cluster.

    Returns:
        Figure Plotly bar chart.
    """
    persona = CLUSTER_PERSONAS[cluster_id]

    if "Education" in df.columns:
        col = "Education"
    elif "Education_Level" in df.columns:
        col = "Education_Level"
    else:
        return go.Figure()

    cluster_data = df[df["Cluster"] == cluster_id]
    counts = cluster_data[col].value_counts().sort_index()
    max_count = counts.max() if len(counts) > 0 else 0

    fig = go.Figure(
        data=[
            go.Bar(
                x=[str(v) for v in counts.index],
                y=counts.values,
                marker_color=persona["color"],
                text=counts.values,
                textposition="outside",
            )
        ]
    )

    _apply_defaults(
        fig,
        title=f"Tingkat Pendidikan — {persona['emoji']} {persona['name']}",
        xaxis=dict(title="Pendidikan"),
        yaxis=dict(
            title="Jumlah",
            gridcolor="rgba(255,255,255,0.1)",
            range=[0, max_count * 1.15] if max_count > 0 else None,
        ),
        height=380,
    )
    return fig


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def _hex_to_rgb(hex_color: str) -> str:
    """Mengkonversi hex color ke format 'R,G,B' untuk rgba()."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{r},{g},{b}"
