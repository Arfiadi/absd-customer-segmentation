"""
app.py — Titik masuk utama aplikasi Customer Segmentation Analytics.

Mengkonfigurasi halaman Streamlit, menerapkan custom CSS,
memeriksa ketersediaan artefak ML, dan mengorkestrasikan 4 tab utama.
"""

import base64
import os
import sys

import streamlit as st

# Pastikan root app ada di sys.path untuk import modular
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import (
    KMEANS_PATH,
    LAYOUT,
    PAGE_ICON,
    PAGE_TITLE,
    PCA_PATH,
    SCALER_PATH,
)
from src.data_loader import load_customer_data
from tabs import dashboard, predictor, profiling, recommendations


# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="collapsed",
)


def load_css(file_name: str) -> None:
    """Membaca file CSS dan menginjeksinya ke aplikasi Streamlit."""
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Custom CSS — Premium Dark Theme
# ---------------------------------------------------------------------------
css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "style.css")
if os.path.exists(css_path):
    load_css(css_path)
else:
    st.warning("⚠️ File style.css tidak ditemukan, menggunakan styling default.")


# ---------------------------------------------------------------------------
# Application Header & Sidebar
# ---------------------------------------------------------------------------
def get_base64_of_bin_file(bin_file: str) -> str:
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
if os.path.exists(logo_path):
    logo_base64 = get_base64_of_bin_file(logo_path)
    img_tag = f'<img src="data:image/png;base64,{logo_base64}" style="width: 40px; height: 40px; border-radius: 8px; margin-right: 12px; object-fit: contain;">'
else:
    img_tag = "📊 "

st.markdown(
    f"""
    <div class="app-header">
        <h1 style="display: flex; align-items: center;">{img_tag} Customer Segmentation Analytics</h1>
        <p>Interactive ML-Powered Customer Intelligence Dashboard</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    with st.expander("⚙️ Model Architecture & Info", expanded=False):
        st.markdown(
            """
            ### Pipeline Details
            - **Algorithm:** K-Means Clustering
            - **Number of Clusters:** 4 (Champion Model B)
            - **Feature Scaling:** `RobustScaler` (28 features)
            - **Dimensionality Reduction:** `PCA` (21 components transformed to 2D/3D visualization)
            
            ---
            *Dashboard ini menggunakan data historis pelanggan yang dikelompokkan menjadi 4 segmen berdasarkan perilaku belanja dan demografis.*
            """
        )


# ---------------------------------------------------------------------------
# Graceful Degradation — Check Model Artifacts
# ---------------------------------------------------------------------------
missing_artifacts = []
for name, path in [
    ("RobustScaler", SCALER_PATH),
    ("PCA Model", PCA_PATH),
    ("KMeans Model", KMEANS_PATH),
]:
    if not os.path.exists(path):
        missing_artifacts.append(f"{name} ({os.path.basename(path)})")

if missing_artifacts:
    st.warning(
        "⚠️ **Artefak ML Pipeline Tidak Ditemukan**\n\n"
        f"File berikut tidak tersedia: {', '.join(missing_artifacts)}.\n\n"
        "Silakan latih model terlebih dahulu dan letakkan file `.pkl` "
        "pada direktori `models/`."
    )
    st.stop()


# ---------------------------------------------------------------------------
# Load Data
# ---------------------------------------------------------------------------
try:
    df = load_customer_data()
except FileNotFoundError:
    st.error(
        "❌ **File data tidak ditemukan.**\n\n"
        "Pastikan `customer_clustered.csv` tersedia di direktori `data/`."
    )
    st.stop()
except Exception as e:
    st.error(f"❌ **Error saat memuat data:** {str(e)}")
    st.stop()

if "Cluster" not in df.columns:
    st.error(
        "❌ Kolom 'Cluster' tidak dapat dihasilkan. "
        "Periksa apakah semua fitur yang diperlukan tersedia di dataset."
    )
    st.stop()


# ---------------------------------------------------------------------------
# Tab Orchestration
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Executive Dashboard",
    "🔍 Persona Profiling",
    "📋 Strategic Recommendations",
    "🤖 Live Predictor",
])

with tab1:
    dashboard.render(df)

with tab2:
    profiling.render(df)

with tab3:
    recommendations.render(df)

with tab4:
    predictor.render(df)
