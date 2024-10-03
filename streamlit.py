import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and preprocess data
df = pd.read_csv(r'C:\Users\ASUS\Downloads\COLLEGE\Semester 7\Bangkit\Tugas\Belajar Analisis Data\bike_sharing_dataset\day.csv')

# Ubah kolom 'dteday' menjadi tipe datetime
df['dteday'] = pd.to_datetime(df['dteday'])
df.set_index('instant', inplace=True)

# Ubah kolom 'weathersit' menjadi fitur kategorikal
df['weathersit'].replace({1: 'Cerah', 2: 'Berkabut', 3: 'Salju Ringan', 4: 'Hujan Deras'}, inplace=True)

# Tambahkan kolom 'user_type' berdasarkan jumlah registered dan casual
df['user_type'] = df.apply(lambda row: 'registered' if row['registered'] > row['casual'] else 'casual', axis=1)

# Load the data
@st.cache_data
def load_data():
    data = df.copy()
    return data

data = load_data()

# Sidebar for filtering
st.sidebar.header('Filter Data')

# Mapping bulan dan weekday untuk label yang lebih mudah dibaca
month_mapping = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 
                 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

weekday_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 
                   4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

# Sidebar selection for month, day of week, and user type
month = st.sidebar.selectbox('Select Month', ['All'] + list(month_mapping.values()))
day_of_week = st.sidebar.selectbox('Select Day of Week', ['All'] + list(weekday_mapping.values()))
user_type = st.sidebar.selectbox('Select User Type', ['All', 'registered', 'casual'])

# Filter the data based on the selection
filtered_data = data.copy()

# Apply month filter if not 'All'
if month != 'All':
    filtered_data = filtered_data[filtered_data['mnth'] == list(month_mapping.keys())[list(month_mapping.values()).index(month)]]

# Apply day of week filter if not 'All'
if day_of_week != 'All':
    filtered_data = filtered_data[filtered_data['weekday'] == list(weekday_mapping.keys())[list(weekday_mapping.values()).index(day_of_week)]]

# Apply user type filter if not 'All'
if user_type != 'All':
    filtered_data = filtered_data[filtered_data['user_type'] == user_type]

# Main Dashboard
st.title('Bike Sharing Analysis Dashboard')

# Deskripsi dataset
st.markdown('''
Sistem berbagi sepeda merupakan evolusi terbaru dari penyewaan sepeda tradisional, di mana seluruh proses mulai dari pendaftaran anggota, penyewaan, hingga pengembalian telah diotomatisasi. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari satu lokasi dan mengembalikannya di lokasi lain. Saat ini, terdapat lebih dari 500 program berbagi sepeda di seluruh dunia, dengan total lebih dari 500 ribu sepeda. Sistem ini kini semakin menarik perhatian karena perannya yang signifikan dalam masalah lalu lintas, lingkungan, dan kesehatan.

Selain aplikasi nyata yang menarik dari sistem berbagi sepeda, karakteristik data yang dihasilkan oleh sistem ini juga menjadikannya menarik untuk penelitian. Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, durasi perjalanan serta lokasi keberangkatan dan kedatangan dicatat secara eksplisit dalam sistem ini. Fitur ini mengubah sistem berbagi sepeda menjadi jaringan sensor virtual yang dapat digunakan untuk mendeteksi mobilitas di kota. Oleh karena itu, diharapkan banyak peristiwa penting di kota dapat terdeteksi melalui pemantauan data ini.
''')


st.title('Pertanyaan?')
st.write(
    """
    - Seberapa sering dan seberapa baru pengguna menyewa sepeda dari sistem bike sharing pada tahun 2011 -2012?
    - Bagaimana karakteristik pengguna kasual dibandingkan dengan pengguna terdaftar dalam hal frekuensi dan waktu penyewaan?
    """
)

st.markdown('## Data Overview')
st.dataframe(filtered_data)

# Ride Count by Temperature
st.markdown('## Ride Count by Temperature')
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x='temp', y='cnt', ax=ax, hue='user_type')
st.pyplot(fig)

# Ride Count by Weather
st.markdown('## Ride Count by Weather')
fig, ax = plt.subplots()
sns.barplot(data=filtered_data, x='weathersit', y='cnt', ax=ax, hue='user_type')
st.pyplot(fig)

st.write('---')

# Pertanyaan 1
st.write(
    """
    ### Seberapa sering dan seberapa baru pengguna menyewa sepeda dari sistem bike sharing pada tahun 2011 -2012?
    Untuk menjawab pertanyaan tersebut, kita perlu menganalisis: 
    1. Frequency => (berapa sering) pengguna menyewa sepeda dan
    2. Recency => (seberapa baru) sewa terakhir mereka.

    Sehingga langkah yang akan ditempuh adalah sebagai berikut:
    1. Frequency: Menghitung total jumlah transaksi (sewa sepeda) yang dilakukan oleh pengguna.
    2. Recency: Menghitung waktu sejak terakhir kali pengguna menyewa sepeda.
    
    """
)

# Visualisasi Jumlah Total Sewa Sepeda Berdasarkan Tahun
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x='yr', y='cnt', estimator=sum, palette='Reds')
plt.title('Total Sewa Sepeda Berdasarkan Tahun (2011-2012)', fontsize=16)
plt.xlabel('Tahun', fontsize=12)
plt.ylabel('Total Sewa Sepeda', fontsize=12)
plt.xticks([0, 1], ['2011', '2012'])
st.pyplot(plt)  # Menampilkan grafik di Streamlit
plt.clf()  # Membersihkan figure agar tidak tumpang tindih di grafik berikutnya

# Expander Penjelasan Visualisasi Jumlah Total Sewa Sepeda Berdasarkan Tahun
with st.expander('See explanation'):
    st.write(
    """
    insight: "Peningkatan Signifikan pada Tahun 2012" 
    
    Terdapat peningkatan yang cukup signifikan dalam jumlah 
    total penyewaan sepeda pada tahun 2012 dibandingkan dengan tahun 2011. Ini mengindikasikan adanya pertumbuhan yang pesat dalam penggunaan layanan bike sharing selama periode tersebut.
    """
    )

# Visualisasi Korelasi Registered dan Casual
plt.figure(figsize=(8, 5))
sns.barplot(x='yr', y='registered', data=df, label='Registered Users', color='blue', width=0.5, errorbar=None)
sns.barplot(x='yr', y='casual', data=df, label='Casual Users', color='red', width=0.5, errorbar=None)
plt.title('Korelasi Registered dan Casual')
plt.xticks([0, 1], ['2011', '2012']) 
plt.xlabel('Year')
plt.ylabel('Rata-Rata Pengguna')
plt.legend()  # Menampilkan legenda untuk grafik
st.pyplot(plt)  # Menampilkan grafik di Streamlit
plt.clf()  # Membersihkan figure agar tidak tumpang tindih di grafik berikutnya

# Expander Penjelasan Visualisasi Korelasi Registered dan Casual
with st.expander('See explanation'):
    st.write(
    """
    insight:
    1. Peningkatan Pengguna Kasual:
    Meskipun tidak sebesar pengguna terdaftar, jumlah pengguna kasual juga mengalami peningkatan. Hal ini mengindikasikan bahwa layanan bike sharing semakin populer dan menarik minat orang untuk mencoba layanan ini meskipun belum menjadi anggota.
    2. Dominasi Pengguna Terdaftar:
    Pada kedua tahun, pengguna terdaftar mendominasi jumlah total pengguna. Ini menunjukkan bahwa model bisnis berbasis keanggotaan cukup efektif dalam menarik dan mempertahankan pelanggan.
    3. Pentingnya Program Keanggotaan: Program keanggotaan yang mengalami lonjakan memberikan kontribusi yang besar terhadap pertumbuhan bisnis rental sepeda. Oleh karena itu, perusahaan perlu terus meningkatkan manfaat dan kemudahan program keanggotaan untuk mempertahankan pengguna yang sudah ada dan menarik lebih banyak pengguna baru.
    4. Potensi Pertumbuhan Pengguna Kasual: Meskipun pengguna terdaftar mendominasi potensi pengguna kasual masih cukup besar. Perusahaan dapat mempertimbangkan strategi untuk mengkonversi pengguna kasual menjadi pengguna terdaftar, misalnya dengan menawarkan program promosi khusus seperti miles pada airlines atau meningkatkan fleksibilitas penggunaan untuk pengguna non-anggota.
    """
    )

# Visualisasi Korelasi Registered dan Casual
plt.figure(figsize=(8, 5))  
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='mnth', y='cnt', estimator=sum, palette='Greens')
plt.title('Total Sewa Sepeda per Bulan', fontsize=16)
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Total Sewa Sepeda', fontsize=12)
plt.xticks(ticks=range(0, 12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'])
plt.show()
st.pyplot(plt)  # Menampilkan grafik di Streamlit
plt.clf()  # Membersihkan figure agar tidak tumpang tindih di grafik berikutnya

with st.expander('See explanation'):
    st.write(
    """
    Insight:
    
1. Puncak Penggunaan: Bulan-bulan Juni, Juli, dan Agustus menunjukkan jumlah penyewaan tertinggi. Ini mengindikasikan bahwa periode liburan dan cuaca yang cerah mendorong lebih banyak orang untuk menggunakan sepeda sebagai alternatif transportasi atau rekreasi.

Sehingga,

>Perusahaan perlu menyesuaikan strategi pemasarannya sesuai dengan musim. Pada bulan-bulan dengan jumlah penyewaan tinggi, fokus dapat diarahkan pada promosi untuk meningkatkan frekuensi penggunaan. Sedangkan pada bulan-bulan dengan jumlah penyewaan rendah, perusahaan dapat menawarkan promo menarik untuk menarik pengguna baru atau mempertahankan pengguna yang sudah ada.

2. Penurunan di Akhir Tahun: Terdapat penurunan yang cukup signifikan pada bulan-bulan terakhir tahun ini (November dan Desember).  Mengingat bahwa data ini berlokasi pada daerah yang mengalami 4 musim, sehingga hal ini mungkin disebabkan oleh cuaca yang semakin dingin dan hari yang semakin pendek, yang membuat orang kurang tertarik untuk bersepeda.

Sehingga,

>Perusahaan dapat mempertimbangkan untuk mengembangkan produk atau layanan tambahan yang dapat menarik pengguna selama musim dingin, seperti aksesori sepeda yang menghangatkan atau program bersepeda indoor.
    """
    )
    
# Visualisasi perbandingan pengguna casual vs registered
df_melt = df.melt(id_vars=['dteday'], value_vars=['casual', 'registered'], var_name='User Type', value_name='Count')
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_melt, x='dteday', y='Count', hue='User Type', palette='Set2')
plt.title('Perbandingan Pengguna Casual vs Registered', fontsize=16)
plt.xticks(rotation=45)
plt.xlabel('Tanggal', fontsize=12)
plt.ylabel('Jumlah Penyewaan', fontsize=12)
st.pyplot(plt)  # Menampilkan grafik di Streamlit
plt.clf()  # Membersihkan figure agar tidak tumpang tindih di grafik berikutnya

# Expander Visualisasi perbandingan pengguna casual vs registered
with st.expander('See explanation'):
    st.write(
    """Insight:
1. Terdapat fluktuasi harian yang signifikan pada jumlah pengguna, baik kasual maupun terdaftar. Ini menunjukkan adanya faktor-faktor harian yang mempengaruhi keputusan pengguna untuk menyewa sepeda, seperti cuaca, hari kerja, dan acara khusus.
2. Ketergantungan pada Cuaca: Fluktuasi harian yang tajam menunjukkan bahwa cuaca memiliki pengaruh yang sangat besar terhadap jumlah penyewaan. Hari-hari yang cerah dan hangat cenderung menarik lebih banyak pengguna.
    """
    )

# Visualisasi Total Sewa Sepeda Berdasarkan Hari dalam Seminggu
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='weekday', y='cnt', estimator=sum, palette='Oranges')
plt.title('Total Sewa Sepeda Berdasarkan Hari dalam Seminggu', fontsize=16)
plt.xlabel('Hari dalam Minggu', fontsize=12)
plt.ylabel('Total Sewa Sepeda', fontsize=12)
plt.xticks(ticks=range(7), labels=['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
plt.show()
st.pyplot(plt)
plt.clf()

# Expander Visualisasi Total Sewa Sepeda Berdasarkan Hari dalam Seminggu
with st.expander('See explanation'):
    st.write(
    """
    insight:
    
    terjadi kenaikan rata-rata peminjaman sepeda pada periode 2011-2012 pada hari senin 
    hingga puncaknya pada hari jumat setiap minggunya dalam periode tersebut. Hal tersebut menandakan, pelanggan banyak meminjam sepeda pada hari workdays dikarenakan mereka lebih banyak beraktivitas diluar rumah seperti bekerja, sekolah, dan berpergian, sedangkan untuk weekend terjadi penurunan karena weekend adalah hari-hari untuk mereka beristirahat.
    """
    )

st.write('---')

# Pertanyaan 2
st.write(
    """
    ### Bagaimana karakteristik pengguna kasual dibandingkan dengan pengguna terdaftar dalam hal frekuensi dan waktu penyewaan? 
    Untuk menjawab pertanyaan ini, kita perlu membandingkan:
    1. Frequency penyewaan antara pengguna kasual dan terdaftar berdasarkan jumlah penyewaan yang dilakukan, dan
    2. Waktu Penyewaan antara kedua tipe pengguna untuk melihat kapan mereka lebih sering menyewa sepeda.
    
    Langkah yang akan ditempuh adalah sebagai berikut:
    1. Frequency: Membandingkan total jumlah penyewaan sepeda yang dilakukan oleh pengguna kasual vs. terdaftar.
    2. Waktu Penyewaan: Menganalisis pola waktu penyewaan untuk kedua tipe pengguna, termasuk hari dalam minggu dan bulan.
    """
)

# 1. Agregasi Total Penyewaan Sepeda Berdasarkan Bulan
df['month'] = df['dteday'].dt.month
monthly_agg = df.groupby('month')[['casual', 'registered']].sum().reset_index()

# 2. Agregasi Total Penyewaan Sepeda Berdasarkan Hari dalam Seminggu
df['weekday_name'] = df['dteday'].dt.day_name()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_agg = df.groupby('weekday_name')[['casual', 'registered']].sum().reset_index()
weekly_agg['weekday_name'] = pd.Categorical(weekly_agg['weekday_name'], categories=weekday_order, ordered=True)
weekly_agg_sorted = weekly_agg.sort_values('weekday_name').reset_index(drop=True)

# 3. Agregasi Total Penyewaan Berdasarkan Workingday dan Holiday
workingday_agg = df.groupby('workingday')[['casual', 'registered']].sum().reset_index()
holiday_agg = df.groupby('holiday')[['casual', 'registered']].sum().reset_index()

# Menampilkan tabel dengan tab
st.markdown(' ### Analisis Frekuensi dan Waktu Penyewaan Sepeda')
st.write('Berdasarkan:')

# Membuat tab untuk setiap tabel
tabs = st.tabs(["Bulanan", "Mingguan", "Workingday dan Holiday"])

# Tabel Agregasi Bulanan
with tabs[0]:
    st.markdown('### 1. Agregasi Total Penyewaan Sepeda Berdasarkan Bulan')
    st.dataframe(monthly_agg)
    st.markdown("""
    **Insight:** 
   
1. Peningkatan Penyewaan Sepeda:

- Terdapat peningkatan signifikan dalam total penyewaan sepeda oleh pengguna terdaftar dari bulan Januari (122.891) hingga bulan Mei (256.401), menunjukkan bahwa semakin banyak orang mendaftar untuk menggunakan layanan bike-sharing.
- Pengguna kasual juga menunjukkan tren peningkatan, dengan jumlah penyewaan tertinggi pada bulan Juni (73.906), meskipun tidak sebanyak pengguna terdaftar.

2. Terjadi Penurunan Penyewaan: 
- Setelah bulan Juni, jumlah penyewaan mulai menurun untuk kedua kategori pengguna, dengan penurunan yang lebih tajam pada bulan November dan Desember. 
-Hal ini menunjukkan bahwa minat terhadap penyewaan sepeda menurun pada bulan-bulan musim dingin, ketika aktivitas luar ruangan berkurang.
    """)
    # Visualisasi Penyewaan Bulanan
    st.markdown('#### Visualisasi Total Penyewaan Sepeda per Bulan (Kasual vs Terdaftar)')
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_agg.plot(x='month', y=['casual', 'registered'], kind='bar', figsize=(10, 6), color=['#990000', '#006c75'], ax=ax)
    ax.set_title('Total Penyewaan Sepeda per Bulan (Pengguna Kasual vs Terdaftar)', fontsize=16)
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Total Penyewaan', fontsize=12)
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'], rotation=45)
    st.pyplot(fig)
    st.write('Terjadi peningkatan penggunaan sepeda dari hari Senin hingga puncaknya pada hari Kamis di setiap minggunya dalam rentang tahun 2011-2012. Hal tersebut menunjukkan bahwa secara umum pelanggan menggunakan layanan sepeda pada sebagian besar workdays hal ini berkaitan pada aktivitas pelanggan pada workdays yang lebih banyak beraktivitas di luar rumah. Sedangkan untuk weekend terjadi penurunan yang mungkin disebabkan oleh aktivitas pelanggan yang berkurang di hari weekend')
   
# Tabel Agregasi Mingguan
with tabs[1]:
    st.markdown('### 2. Agregasi Total Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
    st.dataframe(weekly_agg_sorted)
    st.markdown("""
    **Insight:** 
    
1. Pengguna Kasual Lebih Banyak pada Akhir Pekan
2. Pengguna Terdaftar Dominan pada Hari Kerja
3. Hari Senin Memiliki Jumlah Penyewaan Terendah untuk Pengguna Kasual

Penyewaan sepeda menunjukkan pola yang berbeda antara pengguna kasual dan terdaftar sepanjang minggu. Pengguna kasual cenderung lebih aktif pada akhir pekan, sementara pengguna terdaftar memanfaatkan layanan lebih banyak pada hari kerja.
    """)
    
    # Visualisasi Penyewaan Berdasarkan Hari dalam Minggu
    fig, ax = plt.subplots(figsize=(10, 6))

    # Menggabungkan total casual dan registered agar side-by-side
    weekly_agg_sorted['total'] = weekly_agg_sorted['casual'] + weekly_agg_sorted['registered']

    # Plot casual dan registered sebagai batang terpisah
    ax = sns.barplot(data=weekly_agg_sorted, x='weekday_name', y='total', color='#990000', label='Total', ax=ax)
    sns.barplot(data=weekly_agg_sorted, x='weekday_name', y='casual', color='#006c75', label='Casual', ax=ax)

    ax.set_title('Total Penyewaan Sepeda per Hari dalam Seminggu (Pengguna Kasual vs Terdaftar)', fontsize=16)
    ax.set_xlabel('Hari dalam Minggu', fontsize=12)
    ax.set_ylabel('Total Penyewaan', fontsize=12)
    ax.legend(title='Tipe Pengguna')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
    st.write('')
    st.markdown('Terjadi peningkatan penggunaan sepeda dari hari Senin hingga puncaknya pada hari Kamis di setiap minggunya dalam rentang tahun 2011-2012. Hal tersebut menunjukkan bahwa secara umum pelanggan menggunakan layanan sepeda pada sebagian besar workdays hal ini berkaitan pada aktivitas pelanggan pada workdays yang lebih banyak beraktivitas di luar rumah. Sedangkan untuk weekend terjadi penurunan yang mungkin disebabkan oleh aktivitas pelanggan yang berkurang di hari weekend')

# Tabel Agregasi Berdasarkan Workingday dan Holiday
with tabs[2]:
    st.markdown('### 3. Agregasi Total Penyewaan Berdasarkan Workingday dan Holiday')
    st.dataframe(holiday_agg)
    st.markdown("""
    **Insight:** 
    
1. Signifikan Menurunnya Penyewaan pada Hari Libur
2. Meskipun ada penurunan total penyewaan pada hari libur, pengguna terdaftar masih menyumbang lebih banyak penyewaan dibandingkan pengguna kasual. Hal ini mungkin menunjukkan bahwa pengguna terdaftar memiliki kecenderungan untuk menggunakan sepeda meskipun pada hari libur, yang mungkin dipengaruhi oleh faktor kebutuhan transportasi.
    """)

# Memberi garis pembatas
st.write('----')



# Conclusion
st.markdown('## Conclusion')
st.markdown("""
-  ###  Seberapa sering dan seberapa baru pengguna menyewa sepeda dari sistem bike sharing pada tahun 2011-2012?
 
> Seberapa Sering: Frekuensi penyewaan sepeda sangat bervariasi tergantung pada faktor-faktor seperti musim, hari dalam seminggu, dan cuaca. Secara umum, pengguna cenderung menyewa sepeda lebih sering pada musim panas dan hari-hari yang cerah. Rata-rata peminjaman sepeda terjadi mulai hari senin hingga puncaknya pada hari jumat.

>Seberapa Baru: Grafik ini tidak secara langsung menunjukkan seberapa baru pengguna. Namun, mengingat pertumbuhan jumlah pengguna terdaftar yang signifikan, dapat disimpulkan bahwa terdapat banyak pengguna baru yang bergabung dengan layanan bike sharing selama periode 2011-2012.
""")
st.markdown(
    """
    - ### Bagaimana karakteristik pengguna kasual dibandingkan dengan pengguna terdaftar dalam hal frekuensi dan waktu penyewaan?"

>Secara keseluruhan, pengguna terdaftar  jauh lebih sering dan konsisten dalam penggunaannya dibandingkan  pengguna sesekali. Pengguna biasa cenderung  aktif di luar akhir pekan dan hari libur, sementara pengguna terdaftar menunjukkan pola yang lebih konsisten sepanjang minggu.

>Selain itu, pengguna terdaftar lebih cenderung menyewa sepeda bahkan ketika sedang berlibur, sementara pengguna sesekali cenderung lebih jarang menggunakannya pada saat-saat tersebut. Wawasan ini akan sangat berharga bagi penyedia layanan berbagi sepeda dalam mengembangkan strategi pemasaran dan layanan yang lebih efektif untuk menarik dan mempertahankan dua segmen pengguna: B. Penawaran promosi untuk pengguna biasa dan program loyalitas untuk pengguna terdaftar selama liburan.


    """
)