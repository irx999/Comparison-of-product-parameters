"""主启动页面"""
import streamlit as st

from ui import main_ui

# 设置页面配置
st.set_page_config(page_title="显卡参数对比工具", layout="wide", page_icon="🧊")

main_ui()
