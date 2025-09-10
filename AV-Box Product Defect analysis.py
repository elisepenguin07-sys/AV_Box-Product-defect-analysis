import streamlit as st
import pandas as pd
from io import BytesIO


st.title("Bug Analysis Dashboard")
df = None
uploaded_file = st.file_uploader("Please upload the CSV file to analyze.", type=["csv"])

if uploaded_file is not None:
  try:
    df = pd.read_csv(uploaded_file, encoding = 'utf-8')
  except Exception as e:
    st.error(f"Error reading the file. Please make sure the file is encoded in utf-8.：{e}")

if df is not None:
  summary = df.groupby(['Bug\'s category', '狀態']).size().unstack(fill_value=0)
  summary['Total'] = summary.sum(axis=1)
  
  summary.index.name = None

  output = BytesIO()
  with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
      summary.to_excel(writer, sheet_name='Summary')
  excel_data = output.getvalue()
  
  st.download_button(
    label="📥 Download Bug Summary as Excel",
    data=excel_data,
    file_name='AV-Box Product Defect analysis.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  )
else:
    st.info("Please upload a CSV file to proceed.")
