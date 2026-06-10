# 🎯 Customer Segmentation Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://absd-customer-seg.streamlit.app/)

**🌐 Live Deployment:** [https://absd-customer-seg.streamlit.app/](https://absd-customer-seg.streamlit.app/)

Proyek ini adalah implementasi *end-to-end* dari analisis segmentasi pelanggan menggunakan algoritma **K-Means Clustering** yang dioptimasi dengan **Principal Component Analysis (PCA)** dan **Robust Scaling**. 

Fase riset dan eksperimen dilakukan menggunakan Jupyter Notebook, dan *Champion Model* yang terpilih (berbasis 21 fitur perilaku dan demografi) di-*deploy* ke dalam bentuk aplikasi web interaktif (*Executive Dashboard*) menggunakan **Streamlit**.

## ✨ Fitur Utama (Dashboard Aplikasi)

Aplikasi Streamlit ini dirancang dengan pendekatan *Separation of Concerns* (Modular) dan terbagi menjadi 3 fitur utama:
1. **📊 Executive Dashboard:** Menampilkan metrik KPI makro bisnis, jumlah pelanggan, proporsi persentase ke-4 klaster, dan visualisasi distribusi segmen.
2. **🧬 Cluster Persona :** Menganalisis DNA perilaku dari 4 klaster pelanggan (seperti *The Budget-Conscious Browsers*, dll) secara spesifik untuk tiap klaster.
3. **🔮 Live Predictor:** Fitur *machine learning inference* secara *real-time*. Tim marketing dapat memasukkan data pelanggan baru ke dalam formulir, dan sistem akan memprediksi masuk ke klaster mana pelanggan tersebut.

## 📂 Struktur Tree Proyek

Proyek ini menggunakan arsitektur modular (memisahkan logika UI, backend, dan model) untuk memudahkan *maintenance* dan skalabilitas *deployment*.

```text
absd-customer-segmentation/
│
├── requirements.txt            # Dependensi library untuk deployment cloud (root)
├── notebook/                   # 📓 Eksperimen & Analisis Awal (Jupyter)
├── data/                       # 📂 PENYIMPANAN DATA MENTAH
│
└── streamlit_app/              # 🖥️ APLIKASI WEB STREAMLIT
    ├── app.py                  # 🚀 TITIK MASUK UTAMA (Main Entry Point)
    ├── requirements.txt        # Dependensi aplikasi lokal
    ├── config/                 # ⚙️ Konfigurasi warna, fitur, dan persona klaster
    ├── data/                   # Data CSV hasil clustering
    ├── models/                 # 🧠 Artefak model (.pkl) hasil training
    ├── src/                    # Logika Backend (Data loader, inference, visualizer)
    └── tabs/                   # 🎨 Logika Frontend (Dashboard, Profiling, Predictor)
```

## 🛠️ Instalasi & Cara Menjalankan Aplikasi Lokal

Jika Anda ingin menjalankan aplikasi dashboard Streamlit ini di komputer lokal Anda, ikuti langkah-langkah berikut:

**1. Clone Repositori**

```bash
git clone https://github.com/Arfiadi/absd-customer-segmentation.git
cd absd-customer-segmentation
```

**2. Buat Virtual Environment (Opsional namun sangat direkomendasikan)**

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

**3. Install Dependensi**

```bash
pip install -r requirements.txt
```

**4. Jalankan Aplikasi Streamlit**

```bash
cd streamlit_app
streamlit run app.py
```

Aplikasi akan otomatis terbuka di *browser* Anda pada alamat `http://localhost:8501`.

## 🔬 Catatan Metodologi

Analisis data dilakukan melalui perbandingan berbagai skenario arsitektur fitur. Model final (**Experiment B**) ditetapkan sebagai *Champion Model* dengan spesifikasi:

* **Algoritma:** K-Means
* **Jumlah Fitur:** 21 Fitur (Sinyal Promo Terpusat + Demografi)
* **Preprocessing:** RobustScaler (meredam *outlier* pada nilai finansial) + PCA (Reduksi Dimensi & Mengatasi Multikolinearitas).
* **Performa Metrik:** Silhouette Score = `0.5012` | Davies-Bouldin Index = `0.7714`

*(Untuk detail lengkap mengenai EDA, perbandingan K-Means vs K-Prototypes, dan evaluasi matematis lainnya, silakan lihat file `.ipynb` di dalam repositori ini).*

## 💻 Tech Stack

* **Python 3.x**
* **Machine Learning:** Scikit-Learn
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Plotly, Matplotlib, Seaborn
* **Web Deployment:** Streamlit

```

```
