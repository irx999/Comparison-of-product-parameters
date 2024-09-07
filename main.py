"""主启动文件"""
import json
import streamlit as st
import pandas as pd
from ui import update_ui
# 页面标题






GPU_INFO = pd.read_json("test.json")

print(GPU_INFO)

# 设置页面配置
st.set_page_config(page_title="显卡参数对比工具", layout="wide")






update_ui(GPU_INFO)