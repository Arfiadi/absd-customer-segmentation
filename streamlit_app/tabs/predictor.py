"""
predictor.py — Tab 4: Live Customer Predictor.

Form input terstruktur untuk 21 fitur, dengan validasi,
default values dari median data, dan output prediksi cluster.
"""

import pandas as pd
import streamlit as st

from config.settings import CLUSTER_PERSONAS, EDUCATION_MAP, FEATURES_B, MARITAL_MAP
from src.inference import predict_cluster


def _render_prediction_result(cluster_id: int) -> None:
    """
    Merender hasil prediksi dalam format card yang informatif.

    Args:
        cluster_id: ID cluster hasil prediksi (0-3).
    """
    persona = CLUSTER_PERSONAS[cluster_id]

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {persona['color']}30, {persona['color']}10);
            border: 2px solid {persona['color']};
            border-radius: 12px;
            padding: 28px 32px;
            text-align: center;
            margin: 16px 0;
        ">
            <p style="font-size: 3em; margin: 0;">{persona['emoji']}</p>
            <h2 style="color: {persona['color']}; margin: 8px 0;">
                Cluster {cluster_id}: {persona['name']}
            </h2>
            <p style="color: #aaa; font-size: 1.1em; margin: 4px 0;">
                {persona['subtitle']}
            </p>
            <hr style="border-color: {persona['color']}33; margin: 16px 0;">
            <p style="color: #ccc; line-height: 1.6; text-align: left;">
                {persona['description']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Recommended Actions
    st.markdown(
        f"<h4 style='color:{persona['color']};'>🎯 Recommended Actions</h4>",
        unsafe_allow_html=True,
    )
    for action in persona["marketing_playbook"]:
        st.markdown(f"✅ {action}")


def render(df: pd.DataFrame) -> None:
    """
    Merender konten Tab 4: Live Customer Predictor.

    Menampilkan form input untuk 21 fitur dengan validasi dan default
    values, kemudian menjalankan pipeline inferensi saat disubmit.

    Args:
        df: DataFrame pelanggan untuk menghitung default values.
    """
    st.markdown("### 🤖 Prediksi Segmen Pelanggan Baru")
    st.caption(
        "Masukkan data pelanggan di bawah ini. Semua field sudah terisi "
        "dengan nilai default (median). Sesuaikan sesuai kebutuhan."
    )

    # Compute defaults from data median
    numeric_df = df.select_dtypes(include="number")
    defaults = numeric_df.median().to_dict()

    with st.form("prediction_form", clear_on_submit=False):
        st.markdown("#### 👤 Data Demografis")
        demo_cols = st.columns(3)

        with demo_cols[0]:
            age = st.number_input(
                "Usia (tahun)",
                min_value=18,
                max_value=120,
                value=int(defaults.get("Age", 45)),
                step=1,
                help="Usia pelanggan dalam tahun",
            )
            income = st.number_input(
                "Pendapatan Tahunan ($)",
                min_value=0,
                max_value=700_000,
                value=int(defaults.get("Income", 51000)),
                step=1000,
                help="Pendapatan tahunan rumah tangga",
            )

        with demo_cols[1]:
            education = st.selectbox(
                "Tingkat Pendidikan",
                options=list(EDUCATION_MAP.keys()),
                index=1,
                help="Jenjang pendidikan terakhir",
            )
            marital = st.selectbox(
                "Status Pernikahan",
                options=list(MARITAL_MAP.keys()),
                index=0,
                help="Status relasi / rumah tangga",
            )

        with demo_cols[2]:
            kidhome = st.number_input(
                "Jumlah Anak Kecil",
                min_value=0,
                max_value=5,
                value=int(defaults.get("Kidhome", 0)),
                help="Anak usia < 12 tahun dalam rumah tangga",
            )
            teenhome = st.number_input(
                "Jumlah Remaja",
                min_value=0,
                max_value=5,
                value=int(defaults.get("Teenhome", 0)),
                help="Anak usia 12-18 tahun dalam rumah tangga",
            )
            customer_tenure = st.number_input(
                "Customer Tenure (hari)",
                min_value=0,
                max_value=2000,
                value=int(defaults.get("Customer_Tenure", 350)),
                step=10,
                help="Lama menjadi pelanggan dalam hari",
            )

        st.markdown("---")
        st.markdown("#### 🛍️ Data Pengeluaran Produk ($)")
        spend_cols = st.columns(3)

        with spend_cols[0]:
            mnt_wines = st.number_input(
                "Wines", min_value=0, max_value=2000,
                value=int(defaults.get("MntWines", 175)), step=10,
            )
            mnt_fruits = st.number_input(
                "Fruits", min_value=0, max_value=500,
                value=int(defaults.get("MntFruits", 8)), step=5,
            )

        with spend_cols[1]:
            mnt_meat = st.number_input(
                "Meat Products", min_value=0, max_value=2000,
                value=int(defaults.get("MntMeatProducts", 68)), step=10,
            )
            mnt_fish = st.number_input(
                "Fish Products", min_value=0, max_value=500,
                value=int(defaults.get("MntFishProducts", 12)), step=5,
            )

        with spend_cols[2]:
            mnt_sweet = st.number_input(
                "Sweet Products", min_value=0, max_value=500,
                value=int(defaults.get("MntSweetProducts", 8)), step=5,
            )
            mnt_gold = st.number_input(
                "Gold Products", min_value=0, max_value=500,
                value=int(defaults.get("MntGoldProds", 25)), step=5,
            )

        st.markdown("---")
        st.markdown("#### 📊 Data Perilaku Pembelian")
        behav_cols = st.columns(3)

        with behav_cols[0]:
            web_purchases = st.number_input(
                "Web Purchases", min_value=0, max_value=50,
                value=int(defaults.get("NumWebPurchases", 4)), step=1,
            )
            catalog_purchases = st.number_input(
                "Catalog Purchases", min_value=0, max_value=50,
                value=int(defaults.get("NumCatalogPurchases", 2)), step=1,
            )

        with behav_cols[1]:
            store_purchases = st.number_input(
                "Store Purchases", min_value=0, max_value=50,
                value=int(defaults.get("NumStorePurchases", 5)), step=1,
            )
            web_visits = st.number_input(
                "Web Visits / Bulan", min_value=0, max_value=30,
                value=int(defaults.get("NumWebVisitsMonth", 6)), step=1,
            )

        with behav_cols[2]:
            recency = st.number_input(
                "Recency (hari sejak pembelian terakhir)",
                min_value=0, max_value=200,
                value=int(defaults.get("Recency", 49)), step=1,
            )
            deals_purchases = st.number_input(
                "Deals Purchases", min_value=0, max_value=30,
                value=int(defaults.get("NumDealsPurchases", 2)), step=1,
            )

        st.markdown("---")
        st.markdown("#### 📢 Data Promo & Komplain")
        promo_cols = st.columns(3)

        with promo_cols[0]:
            total_promos = st.number_input(
                "Total Promo Diterima (0-6)",
                min_value=0, max_value=6,
                value=int(defaults.get("Total_Promos", 0)), step=1,
                help="Jumlah total campaign yang direspon (AcceptedCmp1-5 + Response)",
            )

        with promo_cols[1]:
            complain = st.selectbox(
                "Pernah Komplain?",
                options=[0, 1],
                format_func=lambda x: "Ya" if x == 1 else "Tidak",
                index=0,
                help="Apakah pelanggan pernah mengajukan komplain",
            )

        # Submit
        submitted = st.form_submit_button(
            "🚀 Prediksi Segmen Pelanggan",
            width="stretch",
            type="primary",
        )

    # --- Handle Submission ---
    if submitted:
        # Build feature DataFrame
        input_data = {
            "Age": age,
            "Income": float(income),
            "Education_Level": EDUCATION_MAP.get(education, 1),
            "Living_With": MARITAL_MAP.get(marital, 0),
            "Customer_Tenure": customer_tenure,
            "Kidhome": kidhome,
            "Teenhome": teenhome,
            "MntWines": mnt_wines,
            "MntFruits": mnt_fruits,
            "MntMeatProducts": mnt_meat,
            "MntFishProducts": mnt_fish,
            "MntSweetProducts": mnt_sweet,
            "MntGoldProds": mnt_gold,
            "NumWebPurchases": web_purchases,
            "NumCatalogPurchases": catalog_purchases,
            "NumStorePurchases": store_purchases,
            "NumWebVisitsMonth": web_visits,
            "Recency": recency,
            "Total_Promos": total_promos,
            "NumDealsPurchases": deals_purchases,
            "Complain": complain,
        }

        input_df = pd.DataFrame([input_data])

        # Validate feature count
        missing_features = [f for f in FEATURES_B if f not in input_df.columns]
        if missing_features:
            st.error(
                f"⚠️ Fitur berikut tidak tersedia: {missing_features}. "
                "Mohon periksa kembali input Anda."
            )
            return

        # Run prediction
        with st.spinner("Menjalankan pipeline inferensi..."):
            cluster_id = predict_cluster(input_df)

        if cluster_id is not None:
            st.success("✅ Prediksi berhasil!")
            _render_prediction_result(cluster_id)
        else:
            st.error(
                "❌ Terjadi anomali pada pemrosesan input. "
                "Mohon periksa kembali tipe data yang Anda masukkan. "
                "Pastikan semua nilai numerik berada dalam rentang yang logis."
            )
