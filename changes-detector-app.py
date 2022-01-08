import streamlit as st
import pandas as pd
import numpy as np
from bytesbufio import BytesBufferIO
import pyxlsb 
import openpyxl


@st.cache
def to_excel(df):
    output = BytesBufferIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, sheet_name='Sheet1')  # index=False,
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    # format1 = workbook.add_format({'num_format': '0.00'})
    # worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


@st.cache
def highlight_diff(data, color='yellow'):
    attr = 'background-color: {}'.format(color)
    other = data.xs('Previous', axis='columns', level=-1)
    return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                        index=data.index, columns=data.columns)



st.write('# Highlight Changes Between Excel Sheet Version')
st.markdown('#')  
st.write('### This tool will help you spot and compare the changes made in your excel sheet (from previous to current). Simply upload your files and download the outcome.')
st.write('**The app will only accept ".xlsx" files')
st.markdown('#')  

st.write("#### Upload your current file (it will be our KEY file)")
uploaded_file_a = st.file_uploader('File A (Current)',type = ['xlsx'])

st.write("#### Upload your previous file")
uploaded_file_b = st.file_uploader('File B (Previous)',type = ['xlsx'])


if uploaded_file_a is not None:
     if uploaded_file_b is not None:
         st.markdown('#')  
         st.write('### View samples of the data you uploaded')
         dataframe_a = pd.read_excel(uploaded_file_a)
         st.write('#### Current Data Set' )
         st.dataframe(dataframe_a.head(),3000,500)

         dataframe_b = pd.read_excel(uploaded_file_b)
         st.write('#### Previous Data Set')
         st.dataframe(dataframe_b.head(), 3000, 500)

         # """create new dataframe, sort and apply """


         df_all = pd.concat([dataframe_a, dataframe_b], axis='columns', keys=['Current', 'Previous'])

         df_final = df_all.swaplevel(axis='columns')[dataframe_a.columns]
         df_final = df_final.reset_index(inplace = False)

         df_final = df_final.style.apply(highlight_diff, axis=None)

         df_xlsx = to_excel(df_final)

         st.markdown('#')  # see *


         st.write('## Your file is ready!')
         st.download_button(label='📥 Download Your Result',
                            data=df_xlsx,
                            file_name='version_changes.xlsx')
