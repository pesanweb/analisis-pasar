# Analisis Data E-Commerce Olist Brazil

Dashboard interaktif untuk menganalisis data penjualan e-commerce menggunakan Python, Pandas, dan Streamlit.

## 🛠️ Persiapan Environment

### 1. Clone Repository
```bash
git clone https://github.com/<username>/<repo-name>.git
cd analis-pasar
```

### 2. Buat Virtual Environment (Disarankan)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Jika belum ada requirements.txt, install manual:
```bash
pip install pandas numpy matplotlib seaborn streamlit scipy
```

> **Catatan:** Untuk deployment ke Streamlit Cloud, pastikan hanya file `requirements.txt` yang digunakan sebagai referensi dependensi. File `Pipfile` tidak diperlukan dan akan dihapus dari repositori untuk menghindari konflik resolusi dependensi.

## 🚀 Cara Menjalankan

### Local Deployment
```bash
# Clone repository
git clone https://github.com/<username>/<repo-name>.git
cd analis-pasar

# Install dependencies
pip install -r requirements.txt

# Jalankan dashboard Streamlit
streamlit run dashboard/dashboard.py
```

Buka browser ke `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Push ke GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<username>/<repo-name>.git
   git push -u origin main
   ```

2. **Deploy ke Streamlit Cloud**
   - Buka [Streamlit Cloud](https://share.streamlit.io)
   - Login dengan GitHub
   - Klik "New App"
   - Select repository dan branch (main)
   - Main file path: `dashboard/dashboard.py`
   - Klik "Deploy"

3. **Konfigurasi Tambahan (Optional)**  
   File `requirements.txt` sudah tersedia dengan versi kompatibel.

## 📊 Fitur Analisis

### Analisis Dasar
- **Data Gathering**: Memuat 9 dataset CSV (customers, orders, items, payments, reviews, products, sellers, geolocation, category_translation)
- **Assessing Data**: Identifikasi missing values, duplicates, inconsistent values, dan outliers
- **Cleaning Data**: Pembersihan data untuk analisis akurat

### Exploratory Data Analysis (EDA)
- **Online vs Offline Payment Satisfaction** (2017): Perbandingan kepuasan pelanggan antara metode pembayaran online vs offline
- **Konversi Hari Libur vs Hari Kerja** (2018): Analisis perbedaan konversi transaksional saat hari libur nasional vs hari normal
- **Produk Laris**: Kategori produk paling laris dan revenue tertinggi
- **Kota Sumber Cuan**: Kota dengan transaksi dan revenue terbesar

### Teknik Analisis Lanjutan
- **RFM Analysis** - Segmentasi pelanggan berdasarkan Recency, Frequency, Monetary
- **Geospatial Analysis** - Analisis distribusi geografis customer dan seller
- **Clustering** - Manual binning untuk segmentasi berbasis aturan bisnis

## 📁 Struktur File

```
analis-pasar/
├── data/
│   ├── customers_dataset.csv
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── products_dataset.csv
│   ├── sellers_dataset.csv
│   ├── geolocation_trimmed.csv
│   └── product_category_name_translation.csv
├── dashboard/
│   └── dashboard.py             # Streamlit dashboard interaktif
├── Proyek_Analisis_Data.ipynb   # Notebook analisis lengkap
├── requirements.txt             # Dependencies
├── .streamlit/
│   └── config.toml              # Konfigurasi Streamlit
└── README.md                    # File ini
```

## 🎯 Insight Utama

### Pembayaran Online vs Offline (2017)
- Tidak ada perbedaan signifikan kepuasan pelanggan antara metode pembayaran online vs offline
- Fokus pada aspek lain (delivery, kualitas produk) untuk tingkatkan kepuasan

### Konversi Hari Libur vs Hari Kerja (2018)
- Tidak ada perbedaan signifikan konversi transaksional antara hari libur vs hari normal
- Variansi hari normal lebih tinggi → perlu stabilitas proses delivery

### RFM Analysis
- **VIP/Champions**: Pelanggan dengan skor tinggi di semua dimensi - prioritas utama!
- **At Risk**: Pelanggan yang dulu aktif tapi sudah lama tidak beli - perlu campaign win-back

### Geospatial
- Sao Paulo, Rio de Janeiro, Belo Horizonte adalah pasar terbesar
- Perlu ekspansi ke region lain di Brazil

### Clustering
- Mayoritas customer adalah One-time Buyer - opportunity untuk conversion
- Regular + Medium Spender adalah segment paling profitable

## 📝 Lisensi

Dataset berasal dari [Olist E-Commerce Brazil](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) yang tersedia secara gratis.