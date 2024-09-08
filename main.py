"""主启动文件"""
import json
import streamlit as st
import pandas as pd
from ui import product_parameters_comparison

# 设置页面配置
st.set_page_config(page_title="显卡参数对比工具", layout="wide")


#这里需要设置一个侧边栏
st.sidebar.title(">> 1.显卡参数对比工具")
st.sidebar.title(">> 1.CPU参数对比工具- 待开发")




#@st.cache_data
def load_data(excel_file,sheet_name):
    return pd.read_excel(excel_file, sheet_name=sheet_name)



product_parameters_comparison(load_data("product_info.xlsx","GPU"))