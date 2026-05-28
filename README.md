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

## 🚀 Cara Menjalankan

### Local Deployment
```bash
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

## 📊 Fitur Analisis

### Analisis Dasar
- **Data Gathering**: Memuat 9 dataset CSV (customers, orders, items, payments, reviews, products, sellers, geolocation, category_translation)
- **Assessing Data**: Identifikasi missing values, duplicates, inconsistent values, dan outliers
- **Cleaning Data**: Pembersihan data untuk 保证 analisis akurat

### Pertanyaan Bisnis (EDA)
- **Q2**: Kategori produk paling laris dan revenue tertinggi
- **Q3**: Kota sumber cuan terbesar

### Teknik Analisis Lanjutan
- **RFM Analysis** - Segmentasi pelanggan berdasarkan Recency, Frequency, Monetary
- **Geospatial Analysis** - Analisis distribusi geografis customer dan seller
- **Clustering** - Manual binning untuk segmentasi berbasis aturan bisnis

## 🚀 Cara Menjalankan

### Local Deployment

```bash
# Clone repository
git clone <repo-url>
cd analis-pasar

# Install dependencies
pip install -r requirements.txt

# Jalankan dashboard Streamlit
streamlit run dashboard.py
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
   - Main file path: `dashboard.py`
   - Klik "Deploy"

3. **Konfigurasi Tambahan (Optional)**
   
   Buat file `requirements.txt` dengan versi yang kompatibel:
   ```
   pandas>=1.5.0
   numpy>=1.23.0
   matplotlib>=3.6.0
   seaborn>=0.12.0
   streamlit>=1.30.0
   ```

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
└── README.md                    # File ini
```

## 🎯 Insight Utama

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