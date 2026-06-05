"""
app.py — Titik masuk utama aplikasi Customer Segmentation Analytics.

Mengkonfigurasi halaman Streamlit, menerapkan custom CSS,
memeriksa ketersediaan artefak ML, dan mengorkestrasikan 4 tab utama.
"""

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


# ---------------------------------------------------------------------------
# Custom CSS — Premium Dark Theme
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Global typography */
        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
        }

        /* Header styling */
        .app-header {
            background: linear-gradient(135deg, #1a1f2e 0%, #0e1117 50%, #1a1230 100%);
            border-bottom: 1px solid rgba(108, 99, 255, 0.2);
            padding: 24px 32px;
            border-radius: 12px;
            margin-bottom: 24px;
        }
        .app-header h1 {
            background: linear-gradient(135deg, #6C63FF, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2em;
            font-weight: 700;
            margin: 0;
        }
        .app-header p {
            color: #888;
            margin: 4px 0 0;
            font-size: 0.95em;
        }

        /* Metric card enhancement */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #1a1f2e, #151922);
            border: 1px solid rgba(108, 99, 255, 0.15);
            border-radius: 10px;
            padding: 16px 20px;
            transition: transform 0.2s ease, border-color 0.2s ease;
            min-height: 130px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: rgba(108, 99, 255, 0.4);
        }
        [data-testid="stMetricLabel"] {
            color: #888 !important;
            font-size: 0.85em !important;
        }
        [data-testid="stMetricValue"] {
            font-weight: 700 !important;
            font-size: 1.4em !important;
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: rgba(26, 31, 46, 0.5);
            border-radius: 10px;
            padding: 4px;
            width: 100%;
        }
        .stTabs [data-baseweb="tab"] {
            flex-grow: 1;
            text-align: center;
            justify-content: center;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6C63FF33, #6C63FF15);
            border-bottom: 2px solid #6C63FF !important;
        }

        /* Expander enhancement */
        .streamlit-expanderHeader {
            background: rgba(26, 31, 46, 0.6);
            border-radius: 8px;
            font-weight: 500;
        }

        /* Form enhancement */
        [data-testid="stForm"] {
            background: rgba(26, 31, 46, 0.4);
            border: 1px solid rgba(108, 99, 255, 0.1);
            border-radius: 12px;
            padding: 24px;
        }

        /* Divider */
        hr {
            border-color: rgba(108, 99, 255, 0.1) !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0e1117;
        }
        ::-webkit-scrollbar-thumb {
            background: #6C63FF44;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #6C63FF88;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Application Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>📊 Customer Segmentation Analytics</h1>
        <p>Interactive ML-Powered Customer Intelligence Dashboard &middot;
           K-Means (4 Clusters) &middot; PCA &middot; RobustScaler</p>
    </div>
    """,
    unsafe_allow_html=True,
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
