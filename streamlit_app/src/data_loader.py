"""
data_loader.py — Pemuatan dan persiapan data historis pelanggan.

Memuat CSV, melakukan feature engineering yang diperlukan,
dan menambahkan kolom Cluster melalui batch inference.
"""

import logging

import pandas as pd
import streamlit as st

from config.settings import (
    DATA_PATH,
    EDUCATION_MAP,
    FEATURES_B,
    MARITAL_MAP,
    PROMO_COLS,
    PURCHASE_CHANNEL_COLS,
    SPENDING_COLS,
)
from src.inference import predict_cluster_batch

logger = logging.getLogger(__name__)


def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Melakukan feature engineering sesuai pipeline notebook.

    Membuat kolom-kolom turunan yang diperlukan model:
    - Age, Education_Level, Living_With, Customer_Tenure
    - Total_Spent, Total_Purchases, Total_Promos, Total_Children

    Args:
        df: DataFrame mentah dari CSV.

    Returns:
        DataFrame dengan kolom engineered yang lengkap.
    """
    data = df.copy()

    # Age (jika belum ada, hitung dari Year_Birth)
    if "Age" not in data.columns and "Year_Birth" in data.columns:
        data["Age"] = 2014 - data["Year_Birth"]

    # Education_Level
    if "Education_Level" not in data.columns and "Education" in data.columns:
        data["Education_Level"] = data["Education"].map(EDUCATION_MAP).fillna(1)

    # Living_With
    if "Living_With" not in data.columns and "Marital_Status" in data.columns:
        data["Living_With"] = data["Marital_Status"].map(MARITAL_MAP).fillna(0)

    # Customer_Tenure
    if "Customer_Tenure" not in data.columns and "Dt_Customer" in data.columns:
        data["Dt_Customer"] = pd.to_datetime(data["Dt_Customer"], dayfirst=True)
        data["Customer_Tenure"] = (data["Dt_Customer"].max() - data["Dt_Customer"]).dt.days

    # Total_Spent
    if "Total_Spent" not in data.columns:
        available_mnt = [c for c in SPENDING_COLS if c in data.columns]
        if available_mnt:
            data["Total_Spent"] = data[available_mnt].sum(axis=1)

    # Total_Purchases
    if "Total_Purchases" not in data.columns:
        available_purch = [c for c in PURCHASE_CHANNEL_COLS if c in data.columns]
        if available_purch:
            data["Total_Purchases"] = data[available_purch].sum(axis=1)

    # Total_Promos
    if "Total_Promos" not in data.columns:
        available_promo = [c for c in PROMO_COLS if c in data.columns]
        if available_promo:
            data["Total_Promos"] = data[available_promo].sum(axis=1)

    # Total_Children
    if "Total_Children" not in data.columns:
        kid = data.get("Kidhome", 0)
        teen = data.get("Teenhome", 0)
        data["Total_Children"] = kid + teen

    return data


@st.cache_data
def load_customer_data() -> pd.DataFrame:
    """
    Memuat data pelanggan dari CSV, melakukan feature engineering,
    dan menambahkan kolom Cluster melalui batch inference.

    Menggunakan @st.cache_data agar data hanya diproses satu kali.

    Returns:
        DataFrame lengkap dengan kolom Cluster.

    Raises:
        FileNotFoundError: Jika file CSV tidak ditemukan.
    """
    df = pd.read_csv(DATA_PATH)
    logger.info("Loaded %d rows from %s", len(df), DATA_PATH)

    # Feature engineering
    df = _engineer_features(df)

    # Tambahkan kolom Cluster jika belum ada
    if "Cluster" not in df.columns:
        # Pastikan semua 21 fitur tersedia
        missing = [f for f in FEATURES_B if f not in df.columns]
        if missing:
            logger.warning("Missing features for clustering: %s", missing)
        else:
            df["Cluster"] = predict_cluster_batch(df)
            logger.info("Cluster labels assigned via batch inference.")

    return df
