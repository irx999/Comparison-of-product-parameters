"""主启动文件"""
import json
import streamlit as st
import pandas as pd
from ui import product_parameters_comparison
# 页面标题







# 设置页面配置
st.set_page_config(page_title="显卡参数对比工具", layout="wide")






product_parameters_comparison(pd.read_excel("product_info.xlsx", sheet_name="GPU"))