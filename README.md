import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

plt.rcParams['font.family'] = ['Microsoft JhengHei']  # 微軟正黑體，Windows 預設有
plt.rcParams['axes.unicode_minus'] = False

st.title("Bug Tracker Dashboard")
df = None
uploaded_file = st.file_uploader("Please upload the CSV file to analyze.", type=["csv"])

if uploaded_file is not None:
  try:
    df = pd.read_csv(uploaded_file, encoding = 'big5')
  except Exception as e:
    st.error(f"Error reading the file. Please make sure the file is encoded in Big5.：{e}")

if df is not None:
  st.header("🔧 Overview KPIs")
  #All Bug
  st.metric(label="All Bugs", value=df.shape[0])
  #All status
  status_counts = df['狀態'].value_counts().reset_index()
  status_counts.columns = ['Status', 'Count']
  st.table(status_counts)

  #MTTR
  df['建立日期']=pd.to_datetime(df['建立日期'], format='%Y-%m-%d %H:%M')
  df['結束日期']=pd.to_datetime(df['結束日期'], format='%Y-%m-%d %H:%M')
  df['處理天數']=(df['結束日期']-df['建立日期']).dt.days
  df_closed = df.dropna(subset=['結束日期'])
  MTTR = df_closed['處理天數'].mean()
  st.metric(label = "Time to Close(Days)", value = round(MTTR,2))

  #Bug Status Breakdown
  st.header("📊 Diagram Overview")
  plt.figure(figsize=(8, 6))
  sns.countplot(x='狀態', data=df)
  plt.xticks(rotation=45)
  plt.title('Current Bug Status Breakdown')
  st.pyplot(plt)

  #Severity vs Priority Heatmap
  ct = pd.crosstab(df['Severity'], df['優先權'])
  plt.figure(figsize=(8,6))
  sns.heatmap(ct, annot = True, fmt = 'd', cmap='YlGnBu')
  plt.title('Severity vs Priority Heatmap')
  st.pyplot(plt)

  #MTTR
  plt.figure(figsize=(8, 6))
  sns.violinplot(x='優先權', y='處理天數', data=df)
  plt.title("Processing Time Distribution by Priority (Violin Plot)")
  plt.ylabel("Processing Time (days)")
  plt.xlabel("Priority")
  st.pyplot(plt)

else:
    st.info("Please upload a CSV file to proceed.")
