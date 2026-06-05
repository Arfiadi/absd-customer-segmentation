import pandas as pd
import streamlit as st

from config.settings import CLUSTER_COLORS, CLUSTER_PERSONAS


def _render_strategy_card(
    df: pd.DataFrame,
    cluster_id: int,
    expanded: bool = False,
) -> None:
    """
    Merender kartu strategi lengkap untuk satu cluster.

    Menampilkan Marketing Playbook, Retention Strategies, dan
    Omnichannel Approaches dalam format terstruktur.

    Args:
        df: DataFrame pelanggan.
        cluster_id: ID cluster (0-3).
        expanded: Apakah expander terbuka secara default.
    """
    persona = CLUSTER_PERSONAS[cluster_id]

    # Calculate metrics dynamically
    cluster_count = len(df[df["Cluster"] == cluster_id])
    total_count = len(df)
    cluster_percentage = (cluster_count / total_count) * 100 if total_count > 0 else 0

    expander_title = (
        f"{persona['emoji']} **Cluster {cluster_id}: {persona['name']}** | "
        f"{cluster_count:,} users | {cluster_percentage:.1f}% of Population"
    )

    with st.expander(
        expander_title,
        expanded=expanded,
    ):
        # Persona summary
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {persona['color']}15, transparent);
                border-left: 3px solid {persona['color']};
                padding: 12px 16px;
                border-radius: 6px;
                margin-bottom: 16px;
                color: #ccc;
                line-height: 1.6;
            ">
                {persona['description']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Three-column strategy layout
        strat_cols = st.columns(3)

        # Column 1: Marketing Playbook
        with strat_cols[0]:
            st.markdown(
                f"<h4 style='color:{persona['color']};'>🎯 Marketing Playbook</h4>",
                unsafe_allow_html=True,
            )
            for item in persona["marketing_playbook"]:
                st.markdown(f"- {item}")

        # Column 2: Retention Strategies
        with strat_cols[1]:
            st.markdown(
                f"<h4 style='color:{persona['color']};'>🔒 Retention Strategies</h4>",
                unsafe_allow_html=True,
            )
            for item in persona["retention_strategies"]:
                st.markdown(f"- {item}")

        # Column 3: Omnichannel Approaches
        with strat_cols[2]:
            st.markdown(
                f"<h4 style='color:{persona['color']};'>📡 Omnichannel Approaches</h4>",
                unsafe_allow_html=True,
            )
            for item in persona["omnichannel"]:
                st.markdown(f"- {item}")


def _render_key_takeaways() -> None:
    """Merender ringkasan Key Takeaways untuk manajemen."""
    st.markdown("### 💡 Key Takeaways for Management")

    takeaway_cols = st.columns(3)

    with takeaway_cols[0]:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {CLUSTER_COLORS[2]}20, {CLUSTER_COLORS[1]}10);
                border-radius: 10px;
                padding: 20px;
                border: 1px solid {CLUSTER_COLORS[2]}40;
                min-height: 220px;
            ">
                <h4 style="color:{CLUSTER_COLORS[2]};">💰 Fokus Profit</h4>
                <p style="color:#ccc; line-height:1.6;">
                    Prioritaskan <strong>Cluster 2 (Absolute Sultans)</strong> dan
                    <strong>Cluster 1 (Traditional Affluents)</strong> sebagai sumber
                    pendapatan utama. Jaga kualitas layanan, pengalaman pelanggan,
                    dan eksklusivitas produk.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with takeaway_cols[1]:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {CLUSTER_COLORS[3]}20, {CLUSTER_COLORS[3]}05);
                border-radius: 10px;
                padding: 20px;
                border: 1px solid {CLUSTER_COLORS[3]}40;
                min-height: 220px;
            ">
                <h4 style="color:{CLUSTER_COLORS[3]};">📦 Fokus Volume</h4>
                <p style="color:#ccc; line-height:1.6;">
                    Gunakan <strong>Cluster 3 (Smart Veterans)</strong> untuk menjaga
                    perputaran stok melalui strategi promosi yang terarah dan kupon
                    diskon yang ditargetkan.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with takeaway_cols[2]:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {CLUSTER_COLORS[0]}20, {CLUSTER_COLORS[0]}05);
                border-radius: 10px;
                padding: 20px;
                border: 1px solid {CLUSTER_COLORS[0]}40;
                min-height: 220px;
            ">
                <h4 style="color:{CLUSTER_COLORS[0]};">📉 Efisiensi Anggaran</h4>
                <p style="color:#ccc; line-height:1.6;">
                    Kurangi anggaran promosi berbayar untuk <strong>Cluster 0
                    (Budget-Conscious)</strong>. Gunakan pendekatan berbiaya
                    rendah: edukasi produk, konten informatif, dan promosi terbatas.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render(df: pd.DataFrame = None) -> None:
    """
    Merender konten Tab 3: Strategic Business Recommendations.

    Args:
        df: DataFrame pelanggan.
    """
    if df is None:
        from src.data_loader import load_customer_data
        df = load_customer_data()

    st.markdown("### 📋 Rekomendasi Strategi Bisnis per Cluster")
    st.caption(
        "Klik pada setiap cluster untuk melihat detail Marketing Playbook, "
        "Retention Strategies, dan Omnichannel Approaches."
    )

    # Render each cluster strategy card
    for cluster_id in range(4):
        _render_strategy_card(df, cluster_id, expanded=(cluster_id == 0))

    st.divider()

    # Key Takeaways
    _render_key_takeaways()
