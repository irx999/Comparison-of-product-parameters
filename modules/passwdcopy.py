
import streamlit as st
import time
from modules.erp_ui import erp_ui
# 设置密码
PASSWORD = "123"

def pswd():
# 检查用户是否已经登录
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        st.write("欢迎回来！您已经成功登录。")
        erp_ui()
    else:
        # 创建密码输入框
        password = st.text_input("请输入密码", type="password",)

        # 登录按钮
        if st.button("登录"):
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.success("登录成功！")
                st.session_state['password_time'] = time.time()
                st.rerun()
                #st.experimental_set_query_params(page="测试页面")
                # 将登录状态保存1天
            else:
                st.warning("密码错误，请重试。")

        if  password == PASSWORD:
            st.session_state.authenticated = True
            st.success("登录成功！")
            st.session_state['password_time'] = time.time()
            st.rerun()

    # 检查登录状态有效性（1天内）
    if 'password_time' in st.session_state:
        if time.time() - st.session_state['password_time'] > 86400:  # 86400秒 = 1天
            st.session_state.authenticated = False
            del st.session_state['password_time']  # 清除密码时间

    if st.session_state.authenticated:
        pass
        #st.write("这是受保护的内容，仅在您成功登录后可见。")
    else:
        st.write("请先登录来查看受保护的内容。")
