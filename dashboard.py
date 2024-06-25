import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
cust = pd.read_csv('data/olist_customers_dataset.csv')
geo = pd.read_csv('data/olist_geolocation_dataset.csv')
oritems = pd.read_csv('data/olist_order_items_dataset.csv')
orpay = pd.read_csv('data/olist_order_payments_dataset.csv')
orrev = pd.read_csv('data/olist_order_reviews_dataset.csv')
orders = pd.read_csv('data/olist_orders_dataset.csv')
prod = pd.read_csv('data/olist_products_dataset.csv')
sellers = pd.read_csv('data/olist_sellers_dataset.csv')
prodcut = pd.read_csv('data/product_category_name_translation.csv')
cust_items = pd.read_csv('dashboard/cust_items.csv')

# Calculate quartiles and IQR
q25, q75 = np.percentile(cust_items['price'], [25, 75])
iqr = q75 - q25

# Calculate lower and upper bounds for outliers
lower_bound = q25 - (iqr * 1.5)
upper_bound = q75 + (iqr * 1.5)

# Identify outliers
outliers = cust_items[(cust_items['price'] < lower_bound) | (cust_items['price'] > upper_bound)]
num_outliers = len(outliers)

# State descriptions
state_descriptions = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

selected = st.sidebar.selectbox(
    "Home",
    ["Home", "Gathering Data", "Assessing Data", "Cleaning Data", "Exploration & Visualization"]
)

if selected == "Home":
    st.title("Proyek Analisis Data E-Commerce")
    st.markdown(
        """
        # Hello!
        Nama: Revanka Mulya
        Bangkit Email: m002d4ky3274@bangkit.academy
        ID Dicoding:  revanka-mulya

        # Welcome to my dashboard!
        Dashboard ini diperuntukkan proyek analisis data sebagai proses final dari pelatihan analisis data dicoding
        If you have any comment, let me know by contacting me through revankamly@gmail.com

        Dalam proyek ini, digunakan data Brazillian E-Commerce Public Dataset ([Sumber](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce))
        Proyek ini terbagi menjadi beberapa tahap, yaitu
        1. Gathering Data
        2. Assessing Data
        3. Cleaning Data
        4. Exploration & Visualitation

        Proyek ini dilakukan untuk menjawab dua pertanyaan sebagai berikut:
        1. Daerah mana yang memiliki pembeli paliing banyak?
        2. Produk seperti apa yang marak dibeli pada masing-masing daerah?

        Kesimpulan yang dapat diambil dalam proyek ini adalah
        1. Dari visualisasi untuk pertanyaan pertama, kita dapat mengetahui bahwa Sao Paulo merupakan provinsi 
        yang paling banyak melakukan pembelian secara dalam jaringan. Hal ini bisa saja terjadi karena banyak hal, 
        salah satunya karena Sao Paulo merupakan kota besar di Brazil dengan memiliki populasi yang tinggi. 
        Hal ini semakin kuat karena secara kota, Sao Paulo tetap lebih tinggi dibandingkan kota-kota besar lainnya di Brazil 
        dengan perbedaan yang cukup besar.

        2. Dari visualisasi untuk pertanyaan kedua, dapat diketahui bahwa produk yang paling banyak dibeli berupa kebutuhan rumah tangga
        atau kerja. Dapat dilihat pada pie chart dimana 6 kategori produk yang paling banyak dibelinya. 
        Hal ini ditunjukkan pada skala provinsi dan skala kota. Hal ini akan semakin valid jika dapat melihat bagaimana 
        padatnya penduduk yang tinggal di masing-masing provinsi dan kota.

        Dapat dikatakan pembelian terbesar datang dari pelaku rumah tangga di mana mereka menggunakan jasa e-commerce untuk memenuhi kebutuhan hidupnya.

        """
    )

if selected == "Gathering Data":
    st.title("Gathering Data Phase")
    st.markdown(
        """
        Dalam proses Gathering Data, ada beberapa hal penting yang harus dilakukan,
        yaitu:
        1. Mengakses dan membaca data
        2. Melakukan _merging_ data.
        """
    )
    st.subheader(
        """
        Tahap satu,
        mengakses dan membaca data
        """
    )

    # Display the head of the dataframe
    st.write("Berikut 5 data pertama dari olist_customers_dataset:")
    st.dataframe(cust.head())
    st.write("Berikut 5 data pertama dari olist_geolocation_dataset:")
    st.dataframe(geo.head())
    st.write("Berikut 5 data pertama dari olist_order_items_dataset:")
    st.dataframe(oritems.head())
    st.write("Berikut 5 data pertama dari olist_order_payments_dataset:")
    st.dataframe(orpay.head())
    st.write("Berikut 5 data pertama dari olist_order_reviews_dataset:")
    st.dataframe(orrev.head())
    st.write("Berikut 5 data pertama dari olist_orders_dataset:")
    st.dataframe(orders.head())
    st.write("Berikut 5 data pertama dari olist_products_dataset:")
    st.dataframe(prod.head())
    st.write("Berikut 5 data pertama dari olist_sellers_dataset:")
    st.dataframe(sellers.head())
    st.write("Berikut 5 data pertama dari product_category_name_translation:")
    st.dataframe(prodcut.head())

    st.subheader(
        """
        Tahap dua,
        _Merging_ Data,
        """
    )

    # Data preprocessing
    cust.rename(columns={'customer_zip_code_prefix': 'geolocation_zip_code_prefix'}, inplace=True)
    cust_geo = pd.merge(cust, geo, how='right', on='geolocation_zip_code_prefix')
    cust_geo_dropped = cust_geo.drop(
        columns=['geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state'])

    st.write("Merged customer and geolocation data:")
    st.dataframe(cust_geo_dropped.head())

    cust_orders = pd.merge(cust_geo_dropped, orders, how='right', on='customer_id')
    cust_orders_dropped = cust_orders.drop(
        columns=['order_status', 'order_delivered_customer_date', 'order_purchase_timestamp', 'order_approved_at',
                 'order_delivered_carrier_date', 'order_delivered_carrier_date', 'order_estimated_delivery_date'])

    st.write("Merged customer and order data:")
    st.dataframe(cust_orders_dropped.head())

    prod_prodcut = pd.merge(prod, prodcut, how='right', on='product_category_name')
    prod_prodcut_dropped = prod_prodcut.drop(
        columns=['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_height_cm',
                 'product_weight_g', 'product_length_cm', 'product_width_cm'])

    st.write("Merged product and product category translation data:")
    st.dataframe(prod_prodcut_dropped.head())

    oritems_prod_prodcut_dropped = pd.merge(oritems, prod_prodcut_dropped, how='right', on='product_id')
    oritems_prod_prodcut_dropped_dropped = oritems_prod_prodcut_dropped.drop(
        columns=['seller_id', 'shipping_limit_date', 'freight_value'])

    st.write("Merged order items and product data:")
    st.dataframe(oritems_prod_prodcut_dropped_dropped.head())

    cust_orders_dropped_oritems_prod = pd.merge(cust_orders_dropped, oritems_prod_prodcut_dropped_dropped, how='right',
                                                on='order_id')
    cust_items = cust_orders_dropped_oritems_prod

    st.write("Final merged data (customer, orders, and products):")
    st.dataframe(cust_items.head())

    st.write(
        """
        Berikut adalah hasil dari proses _Gathering Data_
        """
    )

if selected == "Assessing Data":
    st.title("Assessing Data Phase")
    st.markdown(
        """
        Dalam proses Assessing Data, ada beberapa hal penting yang harus dilakukan,
        yaitu:
        1. Melakukan penilaian terhadap data-data duplikat
        2. Melakukan penilaian terhadap data-data yang tidak punya nilai
        3. Melakukan pengecekan pada data _outlier_
        """
    )

    st.subheader("Data Duplikat")

    # Memberi label pada program yang akan digunakan
    total_data = len(cust_items)
    data_duplikat = cust_items.duplicated().sum()
    usable_data = total_data - data_duplikat

    # Untuk melihat jumlah data yang merupakan data duplikat dan membandingkannya dengan total data
    st.write(f"Jumlah data: {total_data}")
    st.write(f"Jumlah data duplikat: {data_duplikat}")
    st.write(f"Data yang dapat digunakan: {usable_data}")

    # Untuk melihat jumlah data yang tidak memiliki nilai dan membandingkannya dengan total data
    usable_data_notnull = cust_items.notnull().sum()
    st.write(f"Jumlah data yang tidak memiliki nilai: {usable_data_notnull}")

    # Display the results using Streamlit
    st.write("Calculating outliers based on price column:")
    st.write(f"Lower Quartile (Q1): {q25}")
    st.write(f"Upper Quartile (Q3): {q75}")
    st.write(f"IQR (Interquartile Range): {iqr}")
    st.write(f"Lower Bound for Outliers: {lower_bound}")
    st.write(f"Upper Bound for Outliers: {upper_bound}")
    st.write(f"Number of Outliers: {num_outliers}")

if selected == "Cleaning Data":
    cust_items.drop_duplicates(inplace=True)
    cust_items.dropna(axis=0, inplace=True)
    kondisi_lower_than = cust_items['price'] < lower_bound
    kondisi_more_than = cust_items['price'] > upper_bound
    cust_items.drop(cust_items[kondisi_lower_than].index, inplace=True)
    cust_items.drop(cust_items[kondisi_more_than].index, inplace=True)
    cust_items.tail()  # Menampilkan 5 data terakhir

    # Display the cleaned and filtered data
    st.write("Data setelah proses pembersihan dan filter outlier:")
    st.dataframe(cust_items.tail())

    # Display summary statistics if needed
    st.write("Statistik Deskriptif:")
    st.write(cust_items.describe())

    # Optionally, display the number of records after cleaning and filtering
    st.write(f"Jumlah data yang tersisa setelah pembersihan dan filter outlier: {len(cust_items)}")

if selected == "Exploration & Visualitation":
    # Display info() method result
    st.write("Informasi tentang cust_items:")
    st.write(cust_items.info())

    # Display describe() method result with include='all'
    st.write("Deskripsi statistik tentang cust_items:")
    st.write(cust_items.describe(include='all'))

    st.subheader('Penyebaran pembeli berdasarkan provinsi')
    customer_state_counts = cust_items['customer_state'].value_counts()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x=customer_state_counts.index, height=customer_state_counts.values)
    ax.set_xticks(range(len(customer_state_counts.index)))
    ax.set_xticklabels([state_descriptions.get(state, state) for state in customer_state_counts.index], rotation=90)
    ax.set_title('Penyebaran pembeli berdasarkan provinsi')
    ax.set_xlabel('Provinsi')
    ax.set_ylabel('Jumlah pembeli')
    st.pyplot(fig)

    st.subheader('Penyebaran pembeli berdasarkan kota')
    customer_city_counts = cust_items['customer_city'].value_counts().nlargest(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(y=customer_city_counts.index[::-1], width=customer_city_counts.values[::-1])
    ax.set_title('Penyebaran pembeli berdasarkan kota')
    ax.set_xlabel('Jumlah Pembeli')
    ax.set_ylabel('Kota')
    st.pyplot(fig)

    st.subheader('Distribusi Kategori Produk')
    product_counts = cust_items['product_category_name_english'].value_counts().nlargest(10)
    colors = ['#9b59b6', '#3498db', '#95a5a6', '#e74c3c', '#34495e', '#2ecc71', '#f39c12', '#16a085', '#d35400',
              '#c0392b']
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.pie(product_counts.values, labels=product_counts.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85,
           colors=colors)
    ax.set_title('Distribusi Kategori Produk')
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader('Produk Terbanyak yang Dibeli Berdasarkan Provinsi')
    top_product_by_state = cust_items.groupby(['customer_state', 'product_category_name_english']).size().reset_index(
        name='count')
    top_product_by_state = top_product_by_state.sort_values(by=['customer_state', 'count'], ascending=[True, False])
    total_purchases_per_state = top_product_by_state.groupby('customer_state')['count'].sum().nlargest(5).index
    top_product_by_state_top5 = top_product_by_state[
        top_product_by_state['customer_state'].isin(total_purchases_per_state)]
    top_product_by_state_top5 = top_product_by_state_top5.groupby('customer_state').head(3)
    top_product_by_state_top5['customer_state'] = top_product_by_state_top5['customer_state'].map(state_descriptions)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(data=top_product_by_state_top5, x='customer_state', y='count', hue='product_category_name_english',
                ax=ax)
    ax.set_title('Produk Terbanyak yang Dibeli Berdasarkan Provinsi')
    ax.set_xlabel('Provinsi')
    ax.set_ylabel('Jumlah Pembelian')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.legend(title='Kategori Produk', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.invert_xaxis()
    st.pyplot(fig)

    st.subheader('Produk Terbanyak yang Dibeli Berdasarkan Kota')
    top_product_by_city = cust_items.groupby(['customer_city', 'product_category_name_english']).size().reset_index(
        name='count')
    top_product_by_city = top_product_by_city.sort_values(by=['customer_city', 'count'], ascending=[True, False])
    total_purchases_per_city = top_product_by_city.groupby('customer_city')['count'].sum().nlargest(5).index
    top_product_by_city_top5 = top_product_by_city[top_product_by_city['customer_city'].isin(total_purchases_per_city)]
    top_product_by_city_top5 = top_product_by_city_top5.groupby('customer_city').head(3)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(data=top_product_by_city_top5, x='customer_city', y='count', hue='product_category_name_english', ax=ax)
    ax.set_title('Produk Terbanyak yang Dibeli Berdasarkan Kota')
    ax.set_xlabel('Kota')
    ax.set_ylabel('Jumlah Pembelian')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.legend(title='Kategori Produk', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.invert_xaxis()
    st.pyplot(fig)

    st.write(
        """
        Selesai, terima kasih sudah berkunjung!
        """
    )
