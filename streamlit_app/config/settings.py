"""
settings.py — Pusat konfigurasi aplikasi Customer Segmentation.

Menyimpan semua konstanta, path file, daftar fitur, mapping feature engineering,
dan metadata persona cluster agar mudah dikelola dari satu lokasi.
"""

import os

# ---------------------------------------------------------------------------
# Path Configuration
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

SCALER_PATH = os.path.join(MODELS_DIR, "robust_scaler.pkl")
PCA_PATH = os.path.join(MODELS_DIR, "pca_model.pkl")
KMEANS_PATH = os.path.join(MODELS_DIR, "kmeans_champion.pkl")
DATA_PATH = os.path.join(DATA_DIR, "customer_clustered.csv")

# ---------------------------------------------------------------------------
# Feature Definitions
# ---------------------------------------------------------------------------
# 21 fitur Champion Model (Skenario B) — urutan harus sesuai PCA fit
FEATURES_B = [
    "Age", "Income", "Education_Level", "Living_With", "Customer_Tenure",
    "Kidhome", "Teenhome",
    "MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts",
    "MntSweetProducts", "MntGoldProds",
    "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases",
    "NumWebVisitsMonth", "Recency",
    "Total_Promos", "NumDealsPurchases", "Complain",
]

# 28 fitur yang digunakan untuk fit RobustScaler (superset)
ALL_SCALER_FEATURES = [
    "NumStorePurchases", "Response", "Education_Level", "Age", "Recency",
    "Teenhome", "AcceptedCmp5", "Income", "NumWebPurchases", "AcceptedCmp2",
    "MntWines", "AcceptedCmp3", "MntGoldProds", "NumWebVisitsMonth",
    "MntMeatProducts", "MntFruits", "AcceptedCmp1", "NumDealsPurchases",
    "MntSweetProducts", "Kidhome", "AcceptedCmp4", "Complain", "Living_With",
    "Total_Promos", "NumCatalogPurchases", "MntFishProducts", "Total_Spent",
    "Customer_Tenure",
]

# Kolom pengeluaran per kategori produk
SPENDING_COLS = [
    "MntWines", "MntFruits", "MntMeatProducts",
    "MntFishProducts", "MntSweetProducts", "MntGoldProds",
]

# Kolom pembelian per kanal
PURCHASE_CHANNEL_COLS = [
    "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases",
]

# ---------------------------------------------------------------------------
# Feature Engineering Mappings
# ---------------------------------------------------------------------------
EDUCATION_MAP = {
    "Basic": 0,
    "Graduation": 1,
    "2n Cycle": 2,
    "Master": 2,
    "PhD": 3,
}

EDUCATION_REVERSE_MAP = {0: "Basic", 1: "Graduation", 2: "Master/2n Cycle", 3: "PhD"}

MARITAL_MAP = {
    "Married": 1, "Together": 1,
    "Single": 0, "Divorced": 0, "Widow": 0, "Alone": 0,
    "Absurd": 0, "YOLO": 0,
}

PROMO_COLS = [
    "AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
    "AcceptedCmp4", "AcceptedCmp5", "Response",
]

# ---------------------------------------------------------------------------
# Cluster Persona Metadata
# ---------------------------------------------------------------------------
CLUSTER_COLORS = ["#FF6B6B", "#4ECDC4", "#FFD93D", "#6C63FF"]

CLUSTER_PERSONAS = {
    0: {
        "name": "Budget-Conscious Browsers",
        "subtitle": "Mass Market Segment",
        "emoji": "🛒",
        "color": CLUSTER_COLORS[0],
        "description": (
            "Kelompok ini sering mengunjungi website (±6.26x/bulan) namun tingkat "
            "transaksinya sangat rendah. Pendapatan relatif rendah dengan respon "
            "promosi yang kecil (≈0.16). Fokus pada produk esensial berbiaya rendah."
        ),
        "marketing_playbook": [
            "Tawarkan produk esensial dengan harga ekonomis untuk memicu transaksi pertama.",
            "Gunakan push notification atau email otomatis berbiaya rendah untuk edukasi produk.",
            "Fokuskan promo pada kebutuhan pokok (basic goods) melalui Flash Sales.",
        ],
        "retention_strategies": [
            "Gamification: Berikan poin reward untuk setiap kunjungan website.",
            "Freemium sample produk untuk membangun kebiasaan belanja.",
            "Konten edukatif tentang value-for-money dari produk.",
        ],
        "omnichannel": [
            "📱 Push Notification — Biaya rendah, jangkauan tinggi.",
            "📧 Email Automation — Konten edukasi, bukan iklan agresif.",
            "🌐 Retargeting Ads — Budget terbatas, fokus pada produk esensial.",
        ],
    },
    1: {
        "name": "Traditional Affluents",
        "subtitle": "Store Loyalists",
        "emoji": "🏪",
        "color": CLUSTER_COLORS[1],
        "description": (
            "Segmen penggerak utama trafik toko fisik (Store Purchases tertinggi: ~8.57). "
            "Kanal digital lebih berperan sebagai pendukung. Konsisten membeli produk premium "
            "seperti Wine dan Meat tanpa terlalu bergantung pada diskon."
        ),
        "marketing_playbook": [
            "Tingkatkan pengalaman belanja di toko fisik (Personal Shopper, VIP area).",
            "Optimalkan visual merchandising produk premium untuk impulse buying.",
            "Selenggarakan acara eksklusif (wine tasting, event komunitas).",
        ],
        "retention_strategies": [
            "Program Loyalty tier-based dengan benefit fisik (gratis ongkir, prioritas).",
            "Personal Thank You notes untuk pembelian premium.",
            "Undangan eksklusif ke event pre-launch produk baru.",
        ],
        "omnichannel": [
            "🏬 In-Store Experience — Kanal utama, tingkatkan kualitas layanan.",
            "📬 Katalog Premium — Kirim katalog fisik berkualitas tinggi.",
            "📧 Email Personal — Rekomendasi produk berdasarkan riwayat pembelian.",
        ],
    },
    2: {
        "name": "Absolute Sultans",
        "subtitle": "The Profit Engine",
        "emoji": "👑",
        "color": CLUSTER_COLORS[2],
        "description": (
            "Pelanggan paling menguntungkan dengan pengeluaran besar di hampir semua "
            "kategori produk. Sensitivitas harga sangat rendah (NumDeals terendah: ~1.30). "
            "Memberikan diskon umum justru mengurangi margin profit."
        ),
        "marketing_playbook": [
            "VIP Loyalty Program: Early Access untuk koleksi terbatas + pengiriman prioritas.",
            "Kirimkan penawaran produk premium melalui katalog/email personal eksklusif.",
            "Tawarkan paket bundling premium (Wine + Meat + Gourmet items).",
        ],
        "retention_strategies": [
            "Dedicated Account Manager untuk pelanggan top-tier.",
            "Surprise & Delight: Hadiah tak terduga pada milestone pembelian.",
            "Exclusive preview dan beta testing produk baru.",
        ],
        "omnichannel": [
            "📞 Personal Contact — Dedicated line untuk VIP customers.",
            "📬 Premium Catalog — Materi pemasaran berkualitas tinggi.",
            "🌐 Omni-seamless — Integrasi pengalaman online-offline tanpa hambatan.",
        ],
    },
    3: {
        "name": "Smart Veterans",
        "subtitle": "Deal Hunters",
        "emoji": "🎯",
        "color": CLUSTER_COLORS[3],
        "description": (
            "Pelanggan lama (Tenure tertinggi) yang loyal terhadap brand tetapi sangat "
            "responsif terhadap diskon (NumDeals tertinggi: ~4.34). Aktif menggunakan "
            "website untuk mencari penawaran terbaik sebelum pembelian."
        ),
        "marketing_playbook": [
            "Kupon diskon yang ditargetkan khusus untuk mengoptimalkan perputaran stok.",
            "Promo 'Beli Banyak Lebih Hemat' untuk kategori konsumsi rumah tangga.",
            "Anniversary rewards (voucher/hadiah khusus pada tanggal bergabung).",
        ],
        "retention_strategies": [
            "Loyalty program berbasis poin yang bisa ditukar diskon.",
            "Early notification untuk flash sale dan clearance.",
            "Referral bonus: diskon tambahan untuk setiap pelanggan baru yang dirujuk.",
        ],
        "omnichannel": [
            "🌐 Website — Kanal utama untuk browsing deals.",
            "📱 App Notifications — Alert promo real-time.",
            "📧 Email Newsletter — Kupon mingguan dan deal highlights.",
        ],
    },
}

# ---------------------------------------------------------------------------
# UI Configuration
# ---------------------------------------------------------------------------
PAGE_TITLE = "Customer Segmentation Analytics"
PAGE_ICON = "📊"
LAYOUT = "wide"
