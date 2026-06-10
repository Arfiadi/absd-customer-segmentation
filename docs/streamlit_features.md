# 📊 Panduan Fitur Aplikasi Streamlit: Customer Segmentation Analytics

Aplikasi dashboard ini dibagi menjadi 4 tab utama, yang dirancang sedemikian rupa untuk memandu proses pengambilan keputusan dari tingkatan makro eksekutif hingga tingkatan operasional (seperti melayani pelanggan baru).

Berikut adalah penjelasan fitur-fitur unggulan pada setiap tab:

---

## 📈 Tab 1: Executive Dashboard
Tab ini memberikan pandangan strategis (*helicopter view*) mengenai performa bisnis dan komposisi segmen pelanggan secara keseluruhan.

**Fitur Utama:**
1. **Key Performance Indicators (KPI):** Metrik instan yang menunjukkan status makro: Total Pelanggan, Segmen Dominan, Rata-rata Pendapatan, dan Rata-rata Pengeluaran.
2. **Ringkasan Segmen & Kontribusi Bisnis:** 
   - Grafik Barchart interaktif untuk melihat populasi pelanggan per segmen.
   - Grafik Treemap interaktif untuk melihat seberapa besar proporsi kontribusi *revenue* (pendapatan) dari masing-masing segmen.
3. **Segment Business Insights:**
   - Scatter/Bubble chart interaktif untuk melihat relasi *Engagement* vs *Value* pelanggan antar kelompok.
   - Grafik Barchart bertumpuk untuk melihat komposisi produk mana yang paling laku di setiap *cluster*.

---

## 🔍 Tab 2: Persona Profiling
Tab ini berfungsi sebagai alat investigasi mikroskopik yang memungkinkan tim analis pemasaran untuk "masuk" dan memahami perilaku masing-masing *cluster*.

**Fitur Utama:**
1. **Perbandingan Makro (Snake Plot & Heatmap):** Sebelum memilih 1 segmen, Anda dapat melihat tren relatif semua segmen sekaligus melalui representasi *Snake Plot* atau pola warna *Heatmap*.
2. **Interactive Persona Selector:** Anda dapat memilih 1 dari 4 Persona (contoh: "Absolute Sultans" atau "Budget-Conscious Browsers").
3. **Kartu Statistik Cluster:** Menampilkan kartu deskripsi unik serta perbandingan nilai rata-rata dari cluster yang dipilih *vs* nilai rata-rata global (seluruh populasi).
4. **Analisis Behavioral Khusus:** 
   - Grafik Radar interaktif yang menyorot saluran pembelian apa yang disukai oleh segmen tersebut (apakah mereka suka belanja Web, Toko Fisik, atau via Deals).
   - Grafik Pai (*Donut Chart*) untuk rincian belanja produk.
5. **Analisis Demografis:** Menampilkan persebaran rentang Usia, tingkat Pendidikan, hingga visualisasi pendapatan (Income Boxplot) terhadap segmen lainnya.

---

## 📋 Tab 3: Strategic Recommendations
Sistem tidak hanya memberikan analisis analitik, tetapi juga *actionable insights* (rekomendasi taktis) berdasarkan hasil klasifikasi algoritma.

**Fitur Utama:**
1. **Kartu Strategi Terpadu per Segmen:** Dapat diekspansi untuk melihat rincian:
   - **Marketing Playbook:** Taktik penjualan dan produk seperti apa yang harus diiklankan untuk tipe persona ini.
   - **Retention Strategies:** Cara memelihara relasi (seperti *loyalty program* atau layanan akun personal).
   - **Omnichannel Approaches:** Jalur mana (Email, Katalog Fisik, In-Store) yang sebaiknya digunakan agar *budget marketing* efisien.
2. **Key Takeaways for Management:** Ringkasan level eksekutif yang disesuaikan dalam 3 pilar:
   - **Fokus Profit:** Menentukan cluster mana yang menjadi mesin penghasil profit terbesar.
   - **Fokus Volume:** Menentukan cluster yang memutar stok secara konstan berkat diskon.
   - **Efisiensi Anggaran:** Menentukan segmentasi mana yang promosi berbayarnya harus ditekan agar *Return of Investment* terjaga.

---

## 🤖 Tab 4: Live Predictor
Tab ini mendemonstrasikan implementasi *Machine Learning* dalam kehidupan nyata (*production*). Sangat cocok digunakan oleh tenaga operasional (*sales/customer service*).

**Fitur Utama:**
1. **Dynamic Smart Form:** Formulir untuk meng-input data spesifik seorang pelanggan baru (meliputi Demografi, Riwayat Transaksi Produk, dan Perilaku Belanja). *Field* diisi nilai bawaan (*default*) berupa median data keseluruhan agar simulasi prediksi mudah diuji tanpa harus mengetik banyak angka secara manual.
2. **Real-time Pipeline Inference:** Ketika tombol prediksi diklik, aplikasi menjalankan pipeline clustering secara *live* di latar belakang (`RobustScaler` --> `PCA` --> `KMeans`).
3. **Direct Action Plan Output:** Selain mengembalikan nomor dan nama cluster dari pelanggan tersebut, sistem akan langsung mencetak deskripsi kepribadian dan daftar rekomendasi tindakan apa yang harus segera dilakukan (*Recommended Actions*) untuk memicu pelanggan baru tersebut melakukan pembelian.
