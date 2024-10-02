import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

sns.set_theme(style='whitegrid')

def create_day_df():

    day_df = pd.read_csv("https://raw.githubusercontent.com/Riffaldir/Proyek_Analisis_Data/refs/heads/master/dashboard/day.csv")

    datetime_columns = ["dteday"]
    for column in datetime_columns:
        day_df[column] = pd.to_datetime(day_df[column])
    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()
    return day_df, min_date, max_date

def show_header():
    st.header('Dashboard Bike Sharing')

def sidebar(min_date, max_date):
    with st.sidebar:
        st.subheader('Bike Sharing')
        
        selected_dates = st.date_input(
            label='Rentang Waktu', min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    if len(selected_dates) != 2:
        raise ValueError("Masukkan rentang waktu yang lengkap. Mohon pilih kedua tanggal.")
    start_date, end_date = selected_dates
    return start_date, end_date

def filter_data(day_df, start_date, end_date):
    main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                      (day_df["dteday"] <= str(end_date))]
    return main_df

def show_chart1(day_df):
    st.subheader("Pengaruh suhu terhadap penyewaan")
    korelasi = day_df[['temp', 'cnt']].corr().iloc[0, 1]
    plt.figure(figsize=(12, 6))
    sns.regplot(data=day_df, x='temp', y='cnt', scatter_kws={'s': 100}, line_kws={'color': 'red'})
    plt.title('Hubungan antara Suhu (temp) dan Jumlah Penyewaan (cnt)')
    plt.xlabel('Suhu (Normalized)')
    plt.ylabel('Jumlah Penyewaan')
    plt.grid()
    plt.text(0.7, 300, f'Korelasi: {korelasi:.2f}', fontsize=12, color='blue')
    st.pyplot(plt)

def show_chart2(day_df):
    label_musim = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
    }
    day_df['label_musim'] = day_df['season'].map(label_musim)
    day_df.groupby('label_musim')['cnt'].sum().reset_index().sort_values('cnt')
    
    st.subheader("Musim dengan jumlah penyewaan terbanyak dan sedikit")
    day_df_sorted = day_df.sort_values(by='cnt', ascending=False)
    plt.figure(figsize=(12, 6))
    sns.barplot(x='cnt', y='label_musim', data=day_df_sorted, color='steelblue')  
    plt.title('Total Penyewaan Sepeda')
    plt.xlabel('Jumlah Penyewaan')
    plt.ylabel('Musim')
    plt.xticks(rotation=45)
    st.pyplot(plt)

def show_chart3(day_df):
    st.subheader("Rata-rata penyewaan sepeda per bulan")
    bulan = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
    }
    day_df['mnth'] = day_df['mnth'].map(bulan)
    monthly_avg = day_df.groupby('mnth')['cnt'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='mnth', y='cnt', data=monthly_avg, marker='o', color='blue')
    plt.title('Rata-rata Penyewaan Sepeda per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata Jumlah Penyewaan')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

def main():
    day_df, min_date, max_date = create_day_df()
    start_date, end_date = sidebar(min_date, max_date)
    main_df = filter_data(day_df, start_date, end_date)

    show_header()
    
    col1, col2 = st.columns(2)  
    with col1:
        show_chart1(main_df)  
    with col2:
        show_chart2(main_df)  
    
    show_chart3(day_df)

if __name__ == '__main__':
    main()
