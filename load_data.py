"""数据加载模块"""

import streamlit as st
import pandas as pd


@st.cache_data
def load_data(excel_file:str, sheet_name:str) -> pd.DataFrame:
    """excel文件数据加载"""
    return pd.read_excel(excel_file, sheet_name=sheet_name)





GPU_DATA = load_data('product_data.xlsx', 'GPU')
