'''测试专用文件'''
import streamlit as st
import pandas as pd


# 创建一个包含图片路径的DataFrame
data = {
    'Name': ['Image 1', 'Image 2', 'Image 3'],
    'Image': ['https://irx999.fun/img/HD-Icons/border-radius/Clash_B.png', 'https://irx999.fun/img/HD-Icons/border-radius/Clash_A.png', 'https://irx999.fun/img/HD-Icons/border-radius/Clash_C.png'],
    'URL': ['https://example.com/image1', 'https://example.com/image2', 'https://example.com/image3']
}
df = pd.DataFrame(data)

# 显示DataFrame
st.write("DataFrame with Images:")

# 使用st.columns横向显示图片和名称
cols = st.columns(2)  # 创建两列

for index, row in df.iterrows():
    with cols[index % 2]:  # 交替使用两列
        st.write(f"**{row['Name']}**")
        st.markdown(f"""
        <a href="{row['URL']}" target="_blank">
            <img src="{row['Image']}" style="max-width:100%;">
        </a>
        """, unsafe_allow_html=True)