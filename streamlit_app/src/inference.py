"""
inference.py — Model loading dan pipeline inferensi.

Mengelola pemuatan artefak .pkl (RobustScaler, PCA, KMeans) dengan caching,
serta menyediakan fungsi prediksi untuk single-row dan batch.
"""

import logging
from typing import Optional, Tuple

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from config.settings import (
    ALL_SCALER_FEATURES,
    FEATURES_B,
    KMEANS_PATH,
    PCA_PATH,
    SCALER_PATH,
)

logger = logging.getLogger(__name__)


@st.cache_resource
def load_models() -> Tuple[object, object, object]:
    """
    Memuat tiga artefak model ML dari disk.

    Menggunakan @st.cache_resource agar model hanya dimuat satu kali
    ke dalam RAM selama sesi aplikasi berjalan.

    Returns:
        Tuple berisi (RobustScaler, PCA, KMeans).

    Raises:
        FileNotFoundError: Jika salah satu file .pkl tidak ditemukan.
    """
    scaler = joblib.load(SCALER_PATH)
    pca = joblib.load(PCA_PATH)
    kmeans = joblib.load(KMEANS_PATH)
    logger.info("Model artifacts loaded successfully.")
    return scaler, pca, kmeans


def _prepare_scaler_input(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Menyiapkan DataFrame input agar kompatibel dengan scaler 28-fitur.

    Scaler di-fit pada 28 fitur (ALL_SCALER_FEATURES), namun user hanya
    menginput 21 fitur (FEATURES_B). Kolom tambahan di-fill dengan 0.

    Args:
        input_df: DataFrame dengan kolom sesuai FEATURES_B (21 kolom).

    Returns:
        DataFrame dengan 28 kolom sesuai urutan ALL_SCALER_FEATURES.
    """
    full_df = pd.DataFrame(0, index=input_df.index, columns=ALL_SCALER_FEATURES)
    for col in FEATURES_B:
        if col in input_df.columns:
            full_df[col] = input_df[col].values
    return full_df


def predict_cluster(input_df: pd.DataFrame) -> Optional[int]:
    """
    Menjalankan pipeline inferensi lengkap untuk satu baris data.

    Pipeline: Input (21 fitur) -> Pad ke 28 kolom -> RobustScaler ->
              Slice 21 kolom -> PCA (2 komponen) -> KMeans -> Cluster ID.

    Args:
        input_df: DataFrame single-row dengan 21 kolom FEATURES_B.

    Returns:
        Cluster ID (0-3), atau None jika terjadi error.
    """
    try:
        scaler, pca, kmeans = load_models()

        # Step 1: Pad input to 28 features for scaler compatibility
        full_input = _prepare_scaler_input(input_df)

        # Step 2: Scale
        scaled_full = pd.DataFrame(
            scaler.transform(full_input),
            columns=ALL_SCALER_FEATURES,
            index=input_df.index,
        )

        # Step 3: Slice to 21 features for PCA
        scaled_21 = scaled_full[FEATURES_B]

        # Step 4: PCA transform
        pca_result = pca.transform(scaled_21)

        # Step 5: KMeans predict
        cluster_id = int(kmeans.predict(pca_result)[0])
        return cluster_id

    except Exception as e:
        logger.error("Prediction failed: %s", str(e))
        return None


def predict_cluster_batch(df: pd.DataFrame) -> np.ndarray:
    """
    Menjalankan pipeline inferensi untuk seluruh DataFrame (batch).

    Digunakan saat memuat data historis untuk menambahkan kolom Cluster.

    Args:
        df: DataFrame dengan minimal 21 kolom FEATURES_B.

    Returns:
        Array numpy berisi cluster ID untuk setiap baris.
    """
    scaler, pca, kmeans = load_models()

    full_input = _prepare_scaler_input(df[FEATURES_B])
    scaled_full = pd.DataFrame(
        scaler.transform(full_input),
        columns=ALL_SCALER_FEATURES,
        index=df.index,
    )
    scaled_21 = scaled_full[FEATURES_B]
    pca_result = pca.transform(scaled_21)
    labels = kmeans.predict(pca_result)
    return labels
