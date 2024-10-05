import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
sns.set(style='dark')

def create_Aotizhongxin_COperYear(df):
    ao_yearly_co_df = df.resample(rule='Y', on='datetime').agg({
        "CO":"mean"
    })
    ao_yearly_co_df = ao_yearly_co_df.reset_index()
    ao_yearly_co_df.rename(columns={
        "CO": "Mean CO Levels"
    }, inplace = True)
    return ao_yearly_co_df

def create_Guanyuan_COperYear(df):
    gy_yearly_co_df = df.resample(rule='Y', on='datetime').agg({
        "CO": "mean"
    })
    gy_yearly_co_df = gy_yearly_co_df.reset_index()
    gy_yearly_co_df.rename(columns={
        "CO": "Mean CO Levels"
    }, inplace = True)
    return gy_yearly_co_df

def create_Aotizhongxin_Guanyuan_COperYear(df):
    
    ao_df = df[df['station'] == 'Aotizhongxin']
    gy_df = df[df['station'] == 'Guanyuan']
    
    
    ao_yearly_co = ao_df.resample(rule='Y', on='datetime').agg({"CO": "mean"})
    gy_yearly_co = gy_df.resample(rule='Y', on='datetime').agg({"CO": "mean"})
    
    
    yearly_co_df = pd.merge(
        ao_yearly_co, gy_yearly_co, how='inner', 
        left_index=True, right_index=True, suffixes=('_Aotizhongxin', '_Guanyuan')
    )
    
    yearly_co_df = yearly_co_df.reset_index()
    yearly_co_df.rename(columns={
        "CO_Aotizhongxin": "CO_Aotizhongxin",
        "CO_Guanyuan": "CO_Guanyuan"
    }, inplace=True)
    
    return yearly_co_df

def create_merged_PMNO2mean_df(df):
    yearly_PMNO2_df = df.resample(rule='Y', on='datetime').agg({
        "PM2.5": "mean",  
        "NO2": "mean"       
    })
    yearly_PMNO2_df = yearly_PMNO2_df.reset_index()
    yearly_PMNO2_df.rename(columns={
        "PM2.5": "Mean PM2.5 Levels",
        "NO2": "Mean NO2 Levels"
    }, inplace=True)
    return yearly_PMNO2_df

merged_df = pd.read_csv("merged_df.csv")
datetime_column = ["datetime"]
merged_df.sort_values(by="datetime", inplace=True)
merged_df.reset_index(inplace=True)
for column in datetime_column:
    merged_df[column] = pd.to_datetime(merged_df[column])

min_date = merged_df["datetime"].min()
max_date = merged_df["datetime"].max()
 
with st.sidebar:
    st.image("Air Quality.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = merged_df[(merged_df["datetime"] >= str(start_date)) & 
                (merged_df["datetime"] <= str(end_date))]

Aotizhongxin_COperYear = create_Aotizhongxin_COperYear(main_df)
Guanyuan_COperYear = create_Guanyuan_COperYear(main_df)
Aotizhongxin_Guanyuan_COperYear = create_Aotizhongxin_Guanyuan_COperYear(main_df)
merged_PMNO2_df = create_merged_PMNO2mean_df(main_df)

st.header('Air Quality Dashboard :sparkles:')
st.subheader('Aotizhongxin and Guanyuan CO Levels')

col1, col2 = st.columns(2)

with col1:
    total_years = len(Aotizhongxin_Guanyuan_COperYear["datetime"].unique())
    st.metric("Total Years", value=total_years)
 
with col2:
    total_mean_co = (Aotizhongxin_Guanyuan_COperYear["CO_Aotizhongxin"].mean() + 
                     Aotizhongxin_Guanyuan_COperYear["CO_Guanyuan"].mean()) / 2
    total_mean_co = round(total_mean_co, 2) 
    st.metric("Mean CO Levels", value=total_mean_co)

bar_width = 0.4

r1 = np.arange(len(Aotizhongxin_Guanyuan_COperYear["datetime"].dt.year))
r2 = [x + bar_width for x in r1]

fig, ax = plt.subplots(figsize=(16, 8))

ax.bar(
    r1, 
    Aotizhongxin_Guanyuan_COperYear["CO_Aotizhongxin"], 
    color="#FF9800", 
    width=bar_width, 
    label="Aotizhongxin"
)
ax.bar(
    r2, 
    Aotizhongxin_Guanyuan_COperYear["CO_Guanyuan"], 
    color="#90CAF9", 
    width=bar_width, 
    label="Guanyuan"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xticks([r + bar_width / 2 for r in r1])
ax.set_xticklabels(Aotizhongxin_Guanyuan_COperYear["datetime"].dt.year)
ax.set_xlabel('Year', fontsize=18)
ax.set_ylabel('Mean CO Levels', fontsize=18)
ax.legend(fontsize=15)
st.pyplot(fig)
st.subheader('Aotizhongxin CO Levels')
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    Aotizhongxin_COperYear["datetime"].dt.year, 
    Aotizhongxin_COperYear["Mean CO Levels"],
    color="#FF9800"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
st.subheader('Guanyuan CO Levels')

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    Guanyuan_COperYear["datetime"].dt.year, 
    Guanyuan_COperYear["Mean CO Levels"],
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
st.subheader('Average NO2 and PM2.5 All Station by Year')

bar_width = 0.4

merged_df['datetime'] = pd.to_datetime(merged_df['datetime'])

merged_PMNO2_df = merged_df.resample('Y', on='datetime').agg({
    'NO2': 'mean',
    'PM2.5': 'mean'
}).reset_index()
merged_PMNO2_df['Year'] = merged_PMNO2_df['datetime'].dt.year
r1 = np.arange(len(merged_PMNO2_df['Year']))
r2 = [x + bar_width for x in r1]

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    r1, 
    merged_PMNO2_df['NO2'], 
    color="#90CAF9", 
    width=bar_width, 
    label="NO2"
)
ax.bar(
    r2, 
    merged_PMNO2_df['PM2.5'], 
    color="#FF9800", 
    width=bar_width, 
    label="PM2.5"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xticks([r + bar_width / 2 for r in r1])
ax.set_xticklabels(merged_PMNO2_df['Year'])
ax.set_xlabel('Year', fontsize=18)
ax.set_ylabel('Mean Concentration', fontsize=18)
ax.legend(fontsize=15)
st.pyplot(fig)

st.caption('Nimas Maharani Putri ML-22 Bangkit Academy')