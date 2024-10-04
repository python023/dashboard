import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Baca semua file CSV langsung berdasarkan nama file
file_paths = {
    'PRSA_Data_Nongzhanguan': 'PRSA_Data_Nongzhanguan_20130301-20170228.csv',
    'PRSA_Data_Shunyi': 'PRSA_Data_Shunyi_20130301-20170228.csv',
    'PRSA_Data_Tiantan': 'PRSA_Data_Tiantan_20130301-20170228.csv',
    'PRSA_Data_Aotizhongxin': 'PRSA_Data_Aotizhongxin_20130301-20170228.csv',
    'PRSA_Data_Changping': 'PRSA_Data_Changping_20130301-20170228.csv',
    'PRSA_Data_Dingling': 'PRSA_Data_Dingling_20130301-20170228.csv',
    'PRSA_Data_Dongsi': 'PRSA_Data_Dongsi_20130301-20170228.csv',
    'PRSA_Data_Guanyuan': 'PRSA_Data_Guanyuan_20130301-20170228.csv',
    'PRSA_Data_Gucheng': 'PRSA_Data_Gucheng_20130301-20170228.csv',
    'PRSA_Data_Huairou': 'PRSA_Data_Huairou_20130301-20170228.csv',
    'PRSA_Data_Wanliu': 'PRSA_Data_Wanliu_20130301-20170228.csv',
    'PRSA_Data_Wanshouxigong': 'PRSA_Data_Wanshouxigong_20130301-20170228.csv'
}

# Baca CSV ke dalam DataFrame dan tampilkan informasinya
dataframes = {}
for name, file in file_paths.items():
    df = pd.read_csv(file).drop(columns=['No'], errors='ignore').fillna(0)
    dataframes[name] = df
    st.write(f"### {name}")
    st.write("5 Baris Pertama Data:")
    st.write(df.head())

# Plot harian PM2.5
def plot_daily_pm_trend_and_worst_hour(dataframes):
    plt.figure(figsize=(12, 6))
    
    for name, df in dataframes.items():
        hourly_data = df.groupby('hour').mean(numeric_only=True)
        plt.plot(hourly_data.index, hourly_data['PM2.5'], label=f'{name} - PM2.5')

        worst_hour = hourly_data['PM2.5'].idxmax()
        st.write(f"Stasiun {name}: Kualitas udara paling buruk pada jam {worst_hour}")

    plt.title('Rata-rata Kualitas Udara Harian (PM2.5) di Setiap Jam')
    plt.xlabel('Jam')
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

# Plot scatter antara TEMP dan PM2.5
def plot_temp_vs_pm(dataframes):
    plt.figure(figsize=(12, 6))
    
    for name, df in dataframes.items():
        sns.scatterplot(x='TEMP', y='PM2.5', data=df, label=name)
    
    plt.title('Hubungan antara Suhu (TEMP) dan Polusi Udara (PM2.5)')
    plt.xlabel('Suhu (°C)')
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)')
    plt.legend(loc='upper right')
    plt.grid(True)
    st.pyplot(plt)

# Clustering manual berdasarkan nilai PM2.5
def manual_clustering(df):
    cluster_labels = [1, 2, 3]
    df['Cluster'] = pd.cut(df['PM2.5'], bins=[-1, 50, 150, float('inf')], labels=cluster_labels)
    return df

# Terapkan clustering pada setiap DataFrame
for name, df in dataframes.items():
    dataframes[name] = manual_clustering(df)

# Visualisasi clustering dan hitung jumlah data di setiap cluster
def plot_clustering_and_show_dataframe(dataframes):
    plt.figure(figsize=(10, 6))
    
    for name, df in dataframes.items():
        plt.scatter(df['TEMP'], df['PM2.5'], c=df['Cluster'], label=name, cmap='viridis', alpha=0.5)
        
        st.write(f"DataFrame untuk {name}:")
        st.write(df.head())
        
        cluster_counts = df['Cluster'].value_counts()
        st.write(f"Jumlah data di setiap cluster untuk {name}:")
        st.write(f"Cluster 1 (Polusi Rendah): {cluster_counts.get(1, 0)}")
        st.write(f"Cluster 2 (Polusi Sedang): {cluster_counts.get(2, 0)}")
        st.write(f"Cluster 3 (Polusi Tinggi): {cluster_counts.get(3, 0)}")
    
    plt.title('Clustering PM2.5 Berdasarkan Suhu (TEMP)')
    plt.xlabel('Suhu (°C)')
    plt.ylabel('Konsentrasi PM2.5 (µg/m³)')
    plt.colorbar(label='Cluster')
    plt.grid(True)
    st.pyplot(plt)

# Menampilkan hasil analisis
st.write("## Rata-rata Kualitas Udara Harian dan Jam Paling Buruk")
plot_daily_pm_trend_and_worst_hour(dataframes)

st.write("## Scatter Plot antara Suhu dan Polusi Udara")
plot_temp_vs_pm(dataframes)

st.write("## Hasil Clustering Berdasarkan PM2.5")
plot_clustering_and_show_dataframe(dataframes)
