"""数据加载模块"""

import streamlit as st
import pandas as pd
import base64


@st.cache_data
def load_data(excel_file:str, sheet_name:str) -> pd.DataFrame:
    """excel文件数据加载"""
    return pd.read_excel(excel_file, sheet_name=sheet_name)





GPU_DATA = load_data('product_data.xlsx', 'GPU')



def get_image_base64(image_path):
    """将本地图片转换为 base64 编码的字符串"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
