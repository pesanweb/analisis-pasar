import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard E-Commerce Olist",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Header
st.markdown("""
    <style>
    .big-font { font-size:30px !important; font-weight: bold; }
    .medium-font { font-size:18px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="big-font">🛒 Dashboard Analisis E-Commerce Olist Brazil</p>', unsafe_allow_html=True)
st.markdown('<p class="medium-font">Dashboard ini dibuat dengan bahasa santai ala marketer biar insight-nya gampang dipahami.</p>', unsafe_allow_html=True)
st.markdown("---")

# Load Data
@st.cache_data
def load_data():
    folder = 'data/'
    customers      = pd.read_csv(folder + 'customers_dataset.csv')
    orders         = pd.read_csv(folder + 'orders_dataset.csv')
    items          = pd.read_csv(folder + 'order_items_dataset.csv')
    payments       = pd.read_csv(folder + 'order_payments_dataset.csv')
    reviews        = pd.read_csv(folder + 'order_reviews_dataset.csv')
    products       = pd.read_csv(folder + 'products_dataset.csv')
    sellers        = pd.read_csv(folder + 'sellers_dataset.csv')
    geolocation    = pd.read_csv(folder + 'geolocation_dataset.csv')
    category_trans = pd.read_csv(folder + 'product_category_name_translation.csv')

    # Cleaning sederhana
    date_cols = ['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date',
                 'order_delivered_customer_date','order_estimated_delivery_date']
    for c in date_cols:
        orders[c] = pd.to_datetime(orders[c], errors='coerce')

    customers['customer_city'] = customers['customer_city'].str.lower().str.strip()
    geolocation = geolocation.drop_duplicates()

    mask_delivered = (orders['order_status'] == 'delivered') & (orders['order_delivered_customer_date'].isnull())
    orders_clean = orders[~mask_delivered].copy()

    return customers, orders_clean, items, payments, reviews, products, geolocation, category_trans, sellers

customers, orders, items, payments, reviews, products, geolocation, category_trans, sellers = load_data()

# Sidebar Navigasi
st.sidebar.header("Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Home", "📦 Produk Laris", "📍 Kota Sumber Cuan", "📅 Tren Penjualan", "🚚 Pengiriman & Review", "👥 RFM Analysis", "🗺️ Geospatial", "🎯 Clustering"]
)

# Helper metrics
if menu == "🏠 Home":
    st.header("🏠 Home - Overview")
    st.write("Halaman ini nge-rangkum metrik penting biar lo langsung dapet gambaran besar.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders (Delivered)", f"{len(orders[orders['order_status']=='delivered']):,}")
    col2.metric("Total Revenue (BRL)", f"{items['price'].sum():,.0f}")
    col3.metric("Avg Review Score", f"{reviews['review_score'].mean():.2f}")
    col4.metric("Total Cities", f"{customers['customer_city'].nunique():,}")

    st.markdown("---")
    st.subheader("Distribusi Status Order")
    status_counts = orders['order_status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Jumlah']
    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(data=status_counts.head(6), x='Jumlah', y='Status', palette='magma', ax=ax)
    ax.set_xlabel("Jumlah Order")
    ax.set_ylabel("")
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Metode Pembayaran yang Paling Sering Dipakai")
    pay_counts = payments['payment_type'].value_counts().reset_index()
    pay_counts.columns = ['Payment Type', 'Jumlah']
    fig2, ax2 = plt.subplots(figsize=(8,4))
    sns.barplot(data=pay_counts, x='Jumlah', y='Payment Type', palette='viridis', ax=ax2)
    ax2.set_xlabel("Jumlah Transaksi")
    ax2.set_ylabel("")
    st.pyplot(fig2)

elif menu == "📦 Produk Laris":
    st.header("📦 Produk Laris & Revenue")
    st.write("Di sini kita lihat kategori produk mana yang paling laku dan paling cuan.")

    # Merge data
    items_products = items.merge(products[['product_id','product_category_name']], on='product_id', how='left')
    items_products = items_products.merge(category_trans, on='product_category_name', how='left')
    items_products['product_category_name_english'] = items_products['product_category_name_english'].fillna('unknown')

    q2 = items_products.groupby('product_category_name_english').agg(
        total_items_sold = ('order_item_id', 'count'),
        total_revenue = ('price', 'sum'),
        avg_price = ('price', 'mean')
    ).reset_index().sort_values('total_items_sold', ascending=False)

    tab1, tab2 = st.tabs(["Jumlah Terjual", "Total Revenue"])

    with tab1:
        st.subheader("Top Kategori (by Jumlah Item Terjual)")
        top_n = st.slider("Top N Kategori", min_value=5, max_value=20, value=10)
        top10 = q2.head(top_n)
        fig, ax = plt.subplots(figsize=(10,6))
        bars = ax.barh(top10['product_category_name_english'], top10['total_items_sold'], color='skyblue')
        ax.set_xlabel("Jumlah Item Terjual")
        ax.invert_yaxis()
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, f'{int(width):,}', va='center', ha='left')
        st.pyplot(fig)

    with tab2:
        st.subheader("Top Kategori (by Total Revenue)")
        top_n2 = st.slider("Top N Kategori (Revenue)", min_value=5, max_value=20, value=10)
        top_rev = q2.sort_values('total_revenue', ascending=False).head(top_n2)
        fig2, ax2 = plt.subplots(figsize=(10,6))
        bars2 = ax2.barh(top_rev['product_category_name_english'], top_rev['total_revenue'], color='lightgreen')
        ax2.set_xlabel("Total Revenue (BRL)")
        ax2.invert_yaxis()
        for bar in bars2:
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2, f'{width:,.0f}', va='center', ha='left')
        st.pyplot(fig2)

    st.markdown("---")
    st.info("💡 Insight: Kategori dengan volume tinggi belum tentu revenue tertinggi. Cek strategi harga & bundling-nya ya!")

elif menu == "📍 Kota Sumber Cuan":
    st.header("📍 Kota Sumber Cuan (Customer Location)")
    st.write("Kita lihat dari kota mana aja pembeli terbanyak dan revenue paling gede.")

    cust_orders = customers.merge(orders[['order_id','customer_id','order_status']], on='customer_id', how='inner')
    cust_orders = cust_orders[cust_orders['order_status'] == 'delivered']
    cust_items = cust_orders.merge(items[['order_id','price','freight_value']], on='order_id', how='left')

    q3 = cust_items.groupby('customer_city').agg(
        total_orders = ('order_id', 'nunique'),
        total_revenue = ('price', 'sum'),
        total_freight = ('freight_value', 'sum'),
        avg_order_value = ('price', 'mean')
    ).reset_index().sort_values('total_orders', ascending=False)

    tab1, tab2, tab3 = st.tabs(["Order Terbanyak", "Revenue Terbesar", "Tabel Lengkap"])

    with tab1:
        st.subheader("Top Kota (by Jumlah Unique Orders)")
        top_n = st.slider("Top N Kota", min_value=5, max_value=20, value=10)
        top10 = q3.head(top_n)
        fig, ax = plt.subplots(figsize=(10,6))
        bars = ax.barh(top10['customer_city'], top10['total_orders'], color='salmon')
        ax.set_xlabel("Jumlah Unique Orders")
        ax.invert_yaxis()
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, f'{int(width):,}', va='center', ha='left')
        st.pyplot(fig)

    with tab2:
        st.subheader("Top Kota (by Total Revenue)")
        top_n2 = st.slider("Top N Kota (Revenue)", min_value=5, max_value=20, value=10)
        top_rev = q3.sort_values('total_revenue', ascending=False).head(top_n2)
        fig2, ax2 = plt.subplots(figsize=(10,6))
        bars2 = ax2.barh(top_rev['customer_city'], top_rev['total_revenue'], color='gold')
        ax2.set_xlabel("Total Revenue (BRL)")
        ax2.invert_yaxis()
        for bar in bars2:
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2, f'{width:,.0f}', va='center', ha='left')
        st.pyplot(fig2)

    with tab3:
        st.subheader("Tabel Data Kota")
        st.dataframe(q3.style.format({
            'total_revenue': '{:,.2f}',
            'total_freight': '{:,.2f}',
            'avg_order_value': '{:,.2f}'
        }))

    st.markdown("---")
    st.info("💡 Insight: Sao Paulo jelas mendominasi. Fokuskan budget iklan & promo ke Big 3 kota ini biar ROI makin oke.")

elif menu == "📅 Tren Penjualan":
    st.header("📅 Tren Penjualan Bulanan")
    st.write("Lihat bagaimana performa penjualan dari waktu ke waktu. Ada pattern musiman apa nih?")

    orders['order_month'] = orders['order_purchase_timestamp'].dt.to_period('M')
    monthly_orders = orders.groupby('order_month').agg(
        total_orders = ('order_id', 'count'),
        delivered_orders = ('order_status', lambda x: (x == 'delivered').sum())
    ).reset_index()
    monthly_orders['order_month'] = monthly_orders['order_month'].astype(str)

    items_orders = items.merge(orders[['order_id', 'order_purchase_timestamp']], on='order_id', how='left')
    items_orders['order_month'] = items_orders['order_purchase_timestamp'].dt.to_period('M')
    monthly_revenue = items_orders.groupby('order_month')['price'].sum().reset_index()
    monthly_revenue['order_month'] = monthly_revenue['order_month'].astype(str)

    monthly_merged = monthly_orders.merge(monthly_revenue, on='order_month', how='left')

    tab1, tab2 = st.tabs(["Jumlah Order", "Revenue"])

    with tab1:
        st.subheader("Tren Jumlah Order per Bulan")
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(monthly_merged['order_month'], monthly_merged['total_orders'], marker='o', color='#FF6B6B', linewidth=2)
        ax.plot(monthly_merged['order_month'], monthly_merged['delivered_orders'], marker='s', color='#4ECDC4', linewidth=2, linestyle='--')
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Order")
        ax.legend(['Total Order', 'Delivered'])
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with tab2:
        st.subheader("Tren Revenue per Bulan")
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        ax2.plot(monthly_merged['order_month'], monthly_merged['price'], marker='o', color='#45B7D1', linewidth=2, fillstyle='full')
        ax2.fill_between(monthly_merged['order_month'], monthly_merged['price'], alpha=0.3, color='#45B7D1')
        ax2.set_xlabel("Bulan")
        ax2.set_ylabel("Revenue (BRL)")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    st.markdown("---")
    st.info("💡 Insight: Ada lonjakan orders di bulan November (Black Friday effect). Siapkan stok &客服 yang ekstra!")

elif menu == "🚚 Pengiriman & Review":
    st.header("🚚 Pengiriman & Kepuasan Pelanggan")
    st.write("Apakah kecepatan pengiriman berpengaruh terhadap rating yang diberikan pelanggan?")

    delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
    delivered_orders['delivery_time_days'] = (delivered_orders['order_delivered_customer_date'] - delivered_orders['order_purchase_timestamp']).dt.days

    order_reviews = delivered_orders.merge(reviews[['order_id', 'review_score']], on='order_id', how='inner')
    order_reviews = order_reviews.dropna(subset=['delivery_time_days', 'review_score'])

    tab1, tab2, tab3 = st.tabs(["Delivery Time Distribution", "Review vs Waktu Kirim", "Rata-rata Review per Kota"])

    with tab1:
        st.subheader("Berapa Lama sih Pengiriman?")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(order_reviews['delivery_time_days'], bins=30, kde=True, color='#96CEB4', ax=ax)
        ax.set_xlabel("Hari")
        ax.set_ylabel("Jumlah Order")
        ax.set_title("Distribusi Waktu Pengiriman")
        st.pyplot(fig)
        st.metric("Rata-rata Pengiriman", f"{order_reviews['delivery_time_days'].mean():.1f} hari")

    with tab2:
        st.subheader("Hubungan Waktu Kirim vs Rating")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.boxplot(data=order_reviews, x='review_score', y='delivery_time_days', palette='RdYlGn', ax=ax2)
        ax2.set_xlabel("Review Score")
        ax2.set_ylabel("Waktu Pengiriman (Hari)")
        st.pyplot(fig2)
        corr = order_reviews['delivery_time_days'].corr(order_reviews['review_score'])
        st.write(f"Correlation: **{corr:.3f}** (negative = semakin lama kirim, semakin rendah rating)")

    with tab3:
        st.subheader("Rata-rata Review per Kota Customer (Top 10)")
        review_with_city = order_reviews.merge(customers[['customer_id', 'customer_city']], on='customer_id', how='left')
        city_avg_review = review_with_city.groupby('customer_city')['review_score'].mean().reset_index().sort_values('review_score', ascending=False).head(10)
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        bars = ax3.barh(city_avg_review['customer_city'], city_avg_review['review_score'], color='#FFEAA7')
        ax3.set_xlabel("Average Review Score")
        ax3.set_xlim(0, 5)
        ax3.invert_yaxis()
        st.pyplot(fig3)

    st.markdown("---")
    st.info("💡 Insight: Kalau pengiriman > 20 hari, rating cenderung rendah. Prioritaskan ekspedisi yang lebih cepat untuk kota jauh!")

elif menu == "👥 RFM Analysis":
    st.header("👥 RFM Analysis (Recency, Frequency, Monetary)")
    st.write("Kelompokkan pelanggan berdasarkan perilaku belanja mereka! Yang paling penting: siapa yang baru beli, sering beli, dan banyak uangnya?")

    # Siapkan data untuk RFM
    delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
    cust_orders = customers.merge(delivered_orders[['order_id', 'customer_id', 'order_purchase_timestamp']], on='customer_id', how='inner')
    cust_items = cust_orders.merge(items[['order_id', 'price']], on='order_id', how='left')

    # Hitung reference date (hari terakhir di dataset + 1)
    reference_date = cust_orders['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

    # RFM Aggregation
    rfm = cust_items.groupby('customer_id').agg({
        'order_purchase_timestamp': lambda x: (reference_date - x.max()).days,  # Recency
        'order_id': 'nunique',  # Frequency
        'price': 'sum'  # Monetary
    }).reset_index()
    rfm.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']

    # Binning / Scoring (Manual Scoring 1-5)
    rfm['R_Score'] = pd.cut(rfm['Recency'], bins=5, labels=[5,4,3,2,1])
    rfm['F_Score'] = pd.cut(rfm['Frequency'], bins=5, labels=[1,2,3,4,5])
    rfm['M_Score'] = pd.cut(rfm['Monetary'], bins=5, labels=[1,2,3,4,5])

    rfm['R_Score'] = rfm['R_Score'].astype(int)
    rfm['F_Score'] = rfm['F_Score'].astype(int)
    rfm['M_Score'] = rfm['M_Score'].astype(int)

    # Segmentasi Manual
    def segment_customer(row):
        r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
        if r >= 4 and f >= 4 and m >= 4:
            return 'VIP/Champions'
        elif r >= 3 and f >= 3:
            return 'Loyal Customers'
        elif r >= 3 and f < 3:
            return 'Potential Loyalists'
        elif r >= 4 and m >= 3:
            return 'Big Spenders'
        elif r >= 4:
            return 'Recent Customers'
        elif r <= 2 and f >= 4:
            return 'At Risk'
        elif r <= 2:
            return 'Lost/Hibernating'
        else:
            return 'Others'

    rfm['Segment'] = rfm.apply(segment_customer, axis=1)

    tab1, tab2, tab3 = st.tabs(["RFM Summary", "Customer Segmentation", "Segment Performance"])

    with tab1:
        st.subheader("RFM Distribution")
        col_r, col_f, col_m = st.columns(3)
        with col_r:
            st.metric("Rata-rata Recency", f"{rfm['Recency'].mean():.0f} hari")
        with col_f:
            st.metric("Rata-rata Frequency", f"{rfm['Frequency'].mean():.1f} kali")
        with col_m:
            st.metric("Rata-rata Monetary", f"BRL {rfm['Monetary'].mean():,.0f}")

        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        sns.histplot(rfm['Recency'], bins=30, kde=True, ax=axes[0], color='#FF6B6B')
        axes[0].set_title('Recency Distribution')
        sns.histplot(rfm['Frequency'], bins=30, kde=True, ax=axes[1], color='#4ECDC4')
        axes[1].set_title('Frequency Distribution')
        sns.histplot(rfm['Monetary'], bins=30, kde=True, ax=axes[2], color='#45B7D1')
        axes[2].set_title('Monetary Distribution')
        plt.tight_layout()
        st.pyplot(fig)

    with tab2:
        st.subheader("Customer Segmentation")
        segment_counts = rfm['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Jumlah']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = sns.color_palette('husl', n_colors=len(segment_counts))
        wedges, texts, autotexts = ax.pie(segment_counts['Jumlah'], labels=segment_counts['Segment'], 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Customer Segmentation Distribution')
        st.pyplot(fig)
        
        st.write("**Penjelasan Segment:**")
        st.markdown("""
        - **VIP/Champions:** Beli baru, sering, dan uanggede - prioritas utama!
        - **Loyal Customers:** Sering beli dan masih aktif - jaga baik-baik.
        - **Potential Loyalists:** Baru beli, punya潜在 buat jadi loyal.
        - **Big Spenders:** Uanggede tapi perlu stimulus biar sering beli.
        - **Recent Customers:** Baru beli - perlu di-convert ke regular.
        - **At Risk:** Dulu sering beli, tapi udah lama nggak aktif - perlu outreach.
        - **Lost/Hibernating:** Sudah dorman - sulit diaktifkan, budget营销-nya kecil saja.
        """)

    with tab3:
        st.subheader("Segment Performance (Revenue)")
        segment_rev = rfm.groupby('Segment').agg({
            'Monetary': 'sum',
            'customer_id': 'count'
        }).reset_index()
        segment_rev.columns = ['Segment', 'Total_Revenue', 'Customer_Count']
        segment_rev = segment_rev.sort_values('Total_Revenue', ascending=False)
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        bars = ax2.barh(segment_rev['Segment'], segment_rev['Total_Revenue'], color='mediumseagreen')
        ax2.set_xlabel("Total Revenue (BRL)")
        ax2.invert_yaxis()
        for bar in bars:
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2, f'{width:,.0f}', va='center', ha='left')
        st.pyplot(fig2)

    st.markdown("---")
    st.info("💡 Insight: Fokus ke 'VIP/Champions' dan 'Loyal Customers' untuk maximize revenue. 'At Risk' perlu campaign win-back!")

elif menu == "🗺️ Geospatial":
    st.header("🗺️ Geospatial Analysis")
    st.write("Analisis berdasarkan lokasi geografis! Kita lihat persebaran customer dan seller di seluruh Brazil.")

    # Prepare geolocation data
    geo_clean = geolocation.drop_duplicates(subset=['geolocation_zip_code_prefix'])
    geo_customers = customers.merge(geo_clean, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')
    geo_sellers = sellers.merge(geo_clean, left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')

    # Count per state
    cust_state = customers.groupby('customer_state').size().reset_index(name='customer_count')
    seller_state = sellers.groupby('seller_state').size().reset_index(name='seller_count')
    geo_state = cust_state.merge(seller_state, left_on='customer_state', right_on='seller_state', how='outer').fillna(0)

    tab1, tab2 = st.tabs(["Customer Distribution by State", "Seller Distribution by State"])

    with tab1:
        st.subheader("Customer Distribution (by State)")
        geo_state_sorted = geo_state.sort_values('customer_count', ascending=False).head(15)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(geo_state_sorted['customer_state'], geo_state_sorted['customer_count'], color='#FF6B6B')
        ax.set_xlabel("Jumlah Customer")
        ax.invert_yaxis()
        st.pyplot(fig)
        st.metric("Total States", geo_state['customer_state'].nunique())

    with tab2:
        st.subheader("Seller Distribution (by State)")
        geo_state_sorted2 = geo_state.sort_values('seller_count', ascending=False).head(15)
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        bars2 = ax2.barh(geo_state_sorted2['seller_state'], geo_state_sorted2['seller_count'], color='#4ECDC4')
        ax2.set_xlabel("Jumlah Seller")
        ax2.invert_yaxis()
        st.pyplot(fig2)

    st.markdown("---")
    st.subheader("Customer vs Seller Coverage")
    coverage = geo_state.sort_values('customer_count', ascending=False).head(10)
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    x = np.arange(len(coverage))
    width = 0.35
    ax3.bar(x - width/2, coverage['customer_count'], width, label='Customer', color='#FF6B6B')
    ax3.bar(x + width/2, coverage['seller_count'], width, label='Seller', color='#4ECDC4')
    ax3.set_xticks(x)
    ax3.set_xticklabels(coverage['customer_state'])
    ax3.set_xlabel("State")
    ax3.set_ylabel("Jumlah")
    ax3.legend()
    st.pyplot(fig3)

    st.markdown("---")
    st.info("💡 Insight: Sebagian besar customer di Southeast (SP, RJ, MG). Seller juga dominan di region yang sama. Perlu ekspansi ke region lain!")

elif menu == "🎯 Clustering":
    st.header("🎯 Clustering (Manual Binning)")
    st.write("Kita kelompokkan data berdasarkan karakteristik tertentu tanpa ML! Pakai teknik binning dan manual grouping.")

    # Prepare data
    delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
    cust_orders = customers.merge(delivered_orders[['order_id', 'customer_id', 'order_purchase_timestamp']], on='customer_id', how='inner')
    cust_items = cust_orders.merge(items[['order_id', 'price', 'freight_value']], on='order_id', how='left')

    # Agregat per customer
    customer_stats = cust_items.groupby('customer_id').agg({
        'order_id': 'nunique',
        'price': ['sum', 'mean'],
        'freight_value': 'sum'
    }).reset_index()
    customer_stats.columns = ['customer_id', 'total_orders', 'total_spent', 'avg_order_value', 'total_freight']

    # Binning untuk Order Frequency
    def bin_frequency(x):
        if x == 1:
            return 'One-time Buyer'
        elif x <= 3:
            return 'Regular Buyer (2-3)'
        elif x <= 5:
            return 'Frequent Buyer (4-5)'
        else:
            return 'Super Frequent (>5)'

    customer_stats['Frequency_Cluster'] = customer_stats['total_orders'].apply(bin_frequency)

    # Binning untuk monetary (average order value)
    def bin_monetary(x):
        if x < 50:
            return 'Low Spender'
        elif x < 150:
            return 'Medium Spender'
        elif x < 300:
            return 'High Spender'
        else:
            return 'VIP Spender'

    customer_stats['Monetary_Cluster'] = customer_stats['avg_order_value'].apply(bin_monetary)

    tab1, tab2, tab3 = st.tabs(["Frequency Clustering", "Monetary Clustering", "Cross Analysis"])

    with tab1:
        st.subheader("Customer Clusters by Frequency")
        freq_cluster = customer_stats['Frequency_Cluster'].value_counts().reset_index()
        freq_cluster.columns = ['Cluster', 'Jumlah']
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=freq_cluster, x='Jumlah', y='Cluster', palette='viridis', ax=ax)
        st.pyplot(fig)
        st.write("**Insight:** Kebanyakan customer hanya belanja sekali (One-time Buyer). Ini adalah opportunity untuk conversion!")

    with tab2:
        st.subheader("Customer Clusters by Monetary (Avg Order Value)")
        monetary_cluster = customer_stats['Monetary_Cluster'].value_counts().reset_index()
        monetary_cluster.columns = ['Cluster', 'Jumlah']
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=monetary_cluster, x='Jumlah', y='Cluster', palette='plasma', ax=ax2)
        st.pyplot(fig2)
        st.write("**Insight:** Rata-rata customer termasuk Medium Spender (BRL 50-150 per order). Upselling ke High Spender bisa naikkan revenue!")

    with tab3:
        st.subheader("Cross Analysis: Frequency vs Monetary")
        cross = customer_stats.groupby(['Frequency_Cluster', 'Monetary_Cluster']).size().unstack(fill_value=0)
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.heatmap(cross, annot=True, fmt='d', cmap='YlOrRd', ax=ax3)
        ax3.set_xlabel("Monetary Cluster")
        ax3.set_ylabel("Frequency Cluster")
        st.pyplot(fig3)
        
        st.write("**Best Segment:** Regular Buyer (2-3) + Medium Spender paling banyak. Targetkan mereka buat naikkan frequency!")

    st.markdown("---")
    st.info("💡 Insight: Kombinasi 'One-time Buyer' + 'High Spender' adalah candidate buat email nurture. Kalau sudah frequent & high value, masuk VIP program!")

# Footer
st.markdown("---")
st.caption("© 2024 Analisis E-Commerce Olist | Dibuat dengan Python, Pandas, Matplotlib, Seaborn & Streamlit")
