import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Data
day_df = pd.read_csv("data_day.csv")
hour_df = pd.read_csv("data_hour.csv")

st.title("Dashboard Penyewaan Sepeda")

# Tampilan Data
st.subheader("Tampilkan Data")
option = st.selectbox("Pilih dataset yang ingin ditampilkan:", ["day_df", "hour_df"])

if st.checkbox("Tampilkan Data"):
    if option == "day_df":
        st.write(day_df.head())  # Menampilkan 5 data pertama dari day_df
    else:
        st.write(hour_df.head())  # Menampilkan 5 data pertama dari hour_df

# Korelasi Data
st.subheader("Korelasi antara Jumlah Penyewaan Sepeda dan Variabel Lainnya")

corr_columns = ["cnt", "temp", "atemp", "hum", "windspeed"]
correlation_matrix = day_df[corr_columns].corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)

ax.set_title("Korelasi antara Jumlah Penyewaan Sepeda dan Variabel Lainnya", fontsize=14)
st.pyplot(fig)

# Grafik 1: Pengaruh Cuaca terhadap Penyewaan Sepeda
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
weather_avg = day_df.groupby("weathersit")["cnt"].mean().reset_index()
weather_mapping = {1: "Cerah / Berawan", 2: "Berkabut", 3: "Hujan Ringan / Salju", 4: "Hujan Lebat / Badai"}
weather_avg["weathersit"] = weather_avg["weathersit"].replace(weather_mapping)
max_weather = weather_avg["cnt"].max()
colors = ["#72BCD4" if cnt == max_weather else "#D3D3D3" for cnt in weather_avg["cnt"]]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="weathersit", y="cnt", data=weather_avg, palette=colors, ax=ax)

ax.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda", fontsize=14)
ax.set_xlabel("Cuaca", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)


# Grafik 2: Pengaruh Musim terhadap Penyewaan Sepeda
st.subheader("Analisis Penyewaan Sepeda Berdasarkan Musim")
season_avg = day_df.groupby("season")["cnt"].mean().reset_index()
season_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Salju"}
season_avg["season"] = season_avg["season"].replace(season_mapping)
max_season = season_avg["cnt"].max()

colors = ["#72BCD4" if cnt == max_season else "#D3D3D3" for cnt in season_avg["cnt"]]
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season", y="cnt", data=season_avg, palette=colors, ax=ax)
ax.set_title("Pengaruh Musim terhadap Penyewaan Sepeda", fontsize=14)
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)


# Grafik 3: Penyewaan Sepeda per Jam
st.subheader("Penyewaan Sepeda per Jam")
hourly = hour_df.groupby("hr")["cnt"].sum().reset_index()
fig, ax = plt.subplots()
ax.plot(hourly["hr"], hourly["cnt"], marker='o', color="#72BCD4")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)


# Grafik 4: Distribusi Penyewaan Sepeda pada Hari Kerja dan Libur
st.subheader("Distribusi Penyewaan Sepeda pada Hari Kerja dan Hari Libur")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="workingday", y="cnt", data=day_df, palette=["#72BCD4"], ax=ax)
ax.set_xticklabels(["Hari Libur", "Hari Kerja"])
ax.set_xlabel("Kategori Hari")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Distribusi Penyewaan Sepeda pada Hari Kerja dan Hari Libur")
ax.grid(True, linestyle="--", alpha=0.7)
st.pyplot(fig)


# Grafik 5: Rata-rata Penyewaan Perhari
st.subheader("Rata-rata Penyewaan Sepeda per Hari")

avg_rent_per_day = day_df.groupby("weekday")["cnt"].mean().reset_index()
day_mapping = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}
avg_rent_per_day["weekday"] = avg_rent_per_day["weekday"].replace(day_mapping)
avg_rent_per_day = avg_rent_per_day.sort_values(by="cnt", ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="weekday", y="cnt", data=avg_rent_per_day, color="#72BCD4", ax=ax)

ax.set_title("Rata-rata Penyewaan Sepeda per Hari", fontsize=15)
ax.set_xlabel("Hari", fontsize=12)
ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)
