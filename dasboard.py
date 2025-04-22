import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚲 Bike Sharing Dashboard")

# Load data
df = pd.read_csv('D:\Python_Dicoding\Projekakhir analisis data menggunakan python/hour.csv')
df['dteday'] = pd.to_datetime(df['dteday'])

# Map season & weather
df['season'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
df['weathersit'] = df['weathersit'].map({
    1: 'Clear', 
    2: 'Mist + Cloudy', 
    3: 'Light Snow/Rain', 
    4: 'Heavy Rain/Snow'
})
df['weekend'] = df['weekday'].apply(lambda x: 1 if x in [0, 6] else 0)
df['day_type'] = df['weekend'].map({0: 'Weekday', 1: 'Weekend'})

# Sidebar
st.sidebar.title("🔧 Filter")
day_type_filter = st.sidebar.selectbox("Pilih Jenis Hari", ["All", "Weekday", "Weekend"])

if day_type_filter != "All":
    df = df[df['day_type'] == day_type_filter]

# Tab View
tab1, tab2 = st.tabs(["📈 Peminjaman Sepeda", "🌦️ Pengaruh Cuaca & Lingkungan"])

with tab1:
    st.subheader("Rata-rata Peminjaman per Jam")
    avg_per_hour = df.groupby('hr')['cnt'].mean().reset_index()

    fig1, ax1 = plt.subplots()
    sns.lineplot(data=avg_per_hour, x='hr', y='cnt', marker='o', ax=ax1)
    ax1.set_title("Rata-rata Jumlah Peminjaman Sepeda per Jam")
    ax1.set_xlabel("Jam")
    ax1.set_ylabel("Jumlah Peminjaman")
    ax1.set_xticks(range(0, 24))
    st.pyplot(fig1)

    st.subheader("Peminjaman Sepeda: Weekday vs Weekend")
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=df, x='hr', y='cnt', hue='day_type', ci=None, ax=ax2)
    ax2.set_title("Perbandingan Peminjaman per Jam")
    ax2.set_xlabel("Jam")
    ax2.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig2)

with tab2:
    st.subheader("Jumlah Peminjaman Berdasarkan Cuaca")
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=df, x='weathersit', y='cnt', ax=ax3)
    ax3.set_title("Jumlah Peminjaman per Kondisi Cuaca")
    st.pyplot(fig3)

    st.subheader("Korelasi Suhu, Kelembaban, dan Peminjaman")
    fig4, ax4 = plt.subplots()
    sns.heatmap(df[['temp', 'hum', 'cnt']].corr(), annot=True, cmap='coolwarm', ax=ax4)
    st.pyplot(fig4)

    st.subheader("Scatter Plot: Suhu vs Peminjaman")
    fig5, ax5 = plt.subplots()
    sns.scatterplot(data=df, x='temp', y='cnt', alpha=0.5, ax=ax5)
    ax5.set_title("Suhu vs Jumlah Peminjaman")
    st.pyplot(fig5)
