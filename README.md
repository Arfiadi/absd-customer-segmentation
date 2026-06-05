# 🎯 Customer Segmentation Dashboard

Proyek ini adalah implementasi *end-to-end* dari analisis segmentasi pelanggan menggunakan algoritma **K-Means Clustering** yang dioptimasi dengan **Principal Component Analysis (PCA)** dan **Robust Scaling**. 

Fase riset dan eksperimen dilakukan menggunakan Jupyter Notebook, dan *Champion Model* yang terpilih (berbasis 21 fitur perilaku dan demografi) di-*deploy* ke dalam bentuk aplikasi web interaktif (*Executive Dashboard*) menggunakan **Streamlit**.

## ✨ Fitur Utama (Dashboard Aplikasi)

Aplikasi Streamlit ini dirancang dengan pendekatan *Separation of Concerns* (Modular) dan terbagi menjadi 3 fitur utama:
1. **📊 Executive Dashboard:** Menampilkan metrik KPI makro bisnis, jumlah pelanggan, proporsi persentase ke-4 klaster, dan visualisasi distribusi segmen.
2. **🧬 Cluster Persona &  Recommendation:** Menganalisis perilaku dari 4 klaster pelanggan (seperti *The Budget-Conscious Browsers*, dll) secara spesifik untuk tiap klaster dan memberikan rekomendasi bisnis untuk setiap klaster.
3. **🔮 Live Predictor:** Fitur *machine learning inference* secara *real-time*. Tim marketing dapat memasukkan data pelanggan baru ke dalam formulir, dan sistem akan memprediksi masuk ke klaster mana pelanggan tersebut.

## 📂 Struktur Tree Proyek

Proyek ini menggunakan arsitektur modular (memisahkan logika UI, backend, dan model) untuk memudahkan *maintenance* dan skalabilitas *deployment*.

```text
absd-customer-segmentation/
│
├── app.py                      # 🚀 TITIK MASUK UTAMA (Main Entry Point)
├── requirements.txt            # Daftar dependensi library untuk deployment cloud
├── .gitignore                  # Mengabaikan file sistem, environment, dan model berukuran besar
│
├── data/                       # 📂 PENYIMPANAN DATA
│   ├── marketing_campaign.csv  # Data mentah awal
│   └── customer_clustered.csv  # Data hasil klastering untuk divisualisasikan di Dashboard
│
├── models/                     # 🧠 ARTEFAK AI (Hasil Ekstrak dari Notebook)
│   ├── robust_scaler.pkl       # Scaler untuk 21 fitur
│   ├── pca_model.pkl           # Komponen PCA
│   └── kmeans_champion.pkl     # Model KMeans (4 Klaster)
│
├── src/                        # ⚙️ LOGIKA BACKEND & BANTUAN (Utils)
│   ├── __init__.py             
│   ├── data_loader.py          # Fungsi load data & model (memakai st.cache_data/resource)
│   └── inference_pipeline.py   # Fungsi pemrosesan data input baru -> prediksi klaster
│
└── ui_components/              # 🎨 LOGIKA FRONTEND (Antarmuka Streamlit)
    ├── __init__.py
    ├── tab_dashboard.py        # Kode khusus UI "Executive Dashboard"
    ├── tab_persona.py          # Kode khusus UI "Cluster Persona & MBA"
    └── tab_predictor.py        # Kode khusus UI "Live Predictor"

Berikut adalah draf `README.md` yang profesional, informatif, dan sudah mencakup struktur tree proyek modular Anda. Teks ini ditulis langsung dalam format Markdown sehingga Anda bisa langsung menyalinnya (copy-paste) ke file `README.md` di direktori utama repositori GitHub Anda.

```markdown
# 🎯 AI-Powered Customer Segmentation Dashboard

Proyek ini adalah implementasi *end-to-end* dari analisis segmentasi pelanggan menggunakan algoritma **K-Means Clustering** yang dioptimasi dengan **Principal Component Analysis (PCA)** dan **Robust Scaling**. 

Fase riset dan eksperimen dilakukan menggunakan Jupyter Notebook, dan *Champion Model* yang terpilih (berbasis 21 fitur perilaku dan demografi) di-*deploy* ke dalam bentuk aplikasi web interaktif (*Executive Dashboard*) menggunakan **Streamlit**.

## ✨ Fitur Utama (Dashboard Aplikasi)

Aplikasi Streamlit ini dirancang dengan pendekatan *Separation of Concerns* (Modular) dan terbagi menjadi 3 fitur utama:
1. **📊 Executive Dashboard:** Menampilkan metrik KPI makro bisnis, jumlah pelanggan, proporsi persentase ke-4 klaster, dan visualisasi distribusi segmen.
2. **🧬 Cluster Persona & MBA:** Menganalisis DNA perilaku dari 4 klaster pelanggan (seperti *The Budget-Conscious Browsers*, dll). Menampilkan rata-rata pengeluaran dan *Market Basket Analysis* (aturan asosiasi produk/kampanye) secara spesifik untuk tiap klaster.
3. **🔮 Live Predictor:** Fitur *machine learning inference* secara *real-time*. Tim marketing dapat memasukkan data pelanggan baru ke dalam formulir, dan sistem akan memprediksi masuk ke klaster mana pelanggan tersebut.

## 📂 Struktur Tree Proyek

Proyek ini menggunakan arsitektur modular (memisahkan logika UI, backend, dan model) untuk memudahkan *maintenance* dan skalabilitas *deployment*.

```text
absd-customer-segmentation/
│
├── app.py                      # 🚀 TITIK MASUK UTAMA (Main Entry Point)
├── requirements.txt            # Daftar dependensi library untuk deployment cloud
├── .gitignore                  # Mengabaikan file sistem, environment, dan model berukuran besar
│
├── data/                       # 📂 PENYIMPANAN DATA
│   ├── marketing_campaign.csv  # Data mentah awal
│   └── customer_clustered.csv  # Data hasil klastering untuk divisualisasikan di Dashboard
│
├── models/                     # 🧠 ARTEFAK AI (Hasil Ekstrak dari Notebook)
│   ├── robust_scaler.pkl       # Scaler untuk 21 fitur
│   ├── pca_model.pkl           # Komponen PCA
│   └── kmeans_champion.pkl     # Model KMeans (4 Klaster)
│
├── src/                        # ⚙️ LOGIKA BACKEND & BANTUAN (Utils)
│   ├── __init__.py             
│   ├── data_loader.py          # Fungsi load data & model (memakai st.cache_data/resource)
│   └── inference_pipeline.py   # Fungsi pemrosesan data input baru -> prediksi klaster
│
└── ui_components/              # 🎨 LOGIKA FRONTEND (Antarmuka Streamlit)
    ├── __init__.py
    ├── tab_dashboard.py        # Kode khusus UI "Executive Dashboard"
    ├── tab_persona.py          # Kode khusus UI "Cluster Persona & MBA"
    └── tab_predictor.py        # Kode khusus UI "Live Predictor"

```

## 🛠️ Instalasi & Cara Menjalankan Aplikasi Lokal

Jika Anda ingin menjalankan aplikasi dashboard Streamlit ini di komputer lokal Anda, ikuti langkah-langkah berikut:

**1. Clone Repositori**

```bash
git clone [https://github.com/username-anda/absd-customer-segmentation.git](https://github.com/username-anda/absd-customer-segmentation.git)
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
streamlit run app.py

```

Aplikasi akan otomatis terbuka di *browser* Anda pada alamat `http://localhost:8501`.

## 🔬 Catatan Metodologi Riset

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
