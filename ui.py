'''这里是写UI页面相关'''
import streamlit as st
import pandas as pd

from load_data import GPU_DATA

def main_ui():
    """主页面"""
    params = st.query_params

    # 设置默认页面为显卡参数对比工具
    current_page = params.get("page", ["显卡参数对比工具"])[0]

    # 侧边栏按钮
    def navigate_to(page):
        st.experimental_set_query_params(page=page)
        st.experimental_rerun()

    st.sidebar.button(">> 1. 显卡参数对比工具", on_click=navigate_to, args=("显卡参数对比工具",))
    st.sidebar.button(">> 2. CPU参数对比工具- 待开发", on_click=navigate_to, args=("CPU参数对比工具",))

    # 根据当前页面显示内容
    if current_page == "显卡参数对比工具":
        product_parameters_comparison(GPU_DATA)
    elif current_page == "CPU参数对比工具":
        st.title("CPU参数对比工具 - 待开发")
        # 这里可以添加CPU参数对比工具的代码

def product_parameters_comparison(df: pd.DataFrame):
    '''显卡参数页面'''
    # 页面标题
    st.title('显卡参数对比工具')

    if not df.empty:
        # 提取所有列名作为选项
        column_options = df.columns.tolist()

        # 创建一个列表，用于存放需筛选的东西
        col0, col1, col2 = st.columns(3)
        with col0:
            是否在售 = st.selectbox("是否显示所有显卡型号", ["在售", "已停售", "全部"])
            if 是否在售 == "在售":
                df = df[df["是否在售"] == "在售"]
            elif 是否在售 == "已停售":
                df = df[df["是否在售"] == "not_sale"]
        with col1:
            gpu_column = st.selectbox("选择查看的列", ["简称", "技嘉官网名称", "技嘉规格型号"], index=0)
        with col2:
            筛选框 = st.selectbox("选择筛选项", ["芯片组", "阵营", "系列"], index=0)

        筛选项目 = df[筛选框].unique().tolist()

        col1, col2 = st.columns(2)
        with col1:
            筛选条件 = st.multiselect(f"选择筛选{筛选框}", 筛选项目, default=筛选项目[:3])

        if 筛选条件:
            df = df[df[筛选框].isin(筛选条件)]

        # 选择显卡型号列后，从该列中选择具体的显卡型号
        gpu_options = df[gpu_column].unique().tolist()
        parameter_options = [col for col in column_options if col != gpu_column]
        with col2:
            # 去除显卡型号列，剩余的是参数列
            selected_params = st.multiselect("选择参数进行对比（如果不选，默认展示所有参数)",
                                             parameter_options,
                                             default=None
                                             )

        selected_gpus = st.multiselect("选择要对比的显卡型号",
                                       gpu_options,
                                       default=gpu_options[:10])

        # 如果用户选择了显卡型号，过滤数据
        if selected_gpus:
            df = df[df[gpu_column].isin(selected_gpus)]
        st.write(f"显卡型号：{gpu_column}")
        st.write(f"展示的参数：{', '.join(selected_params) if selected_params else '所有参数'}")

        # 构建展示数据的 DataFrame，行是显卡型号，列是选中的参数
        df["技嘉规格型号copy"] = df["技嘉规格型号"]
        if selected_params:
            display_data = df[[gpu_column] + selected_params + ["技嘉规格型号copy"]+["Image"]].set_index(gpu_column)
        else:
            display_data = df.set_index(gpu_column)
        if selected_gpus:
            cols = st.columns([0.5] + [1] * len(selected_gpus))
            with cols[0]:
                st.write("显卡图片：")
            for index, row in display_data.iterrows():
                with cols[selected_gpus.index(index) + 1]:
                    set_image_width = 100 if len(selected_gpus) > 3 else 50
                    st.markdown(f"""
                    <a href="https://www.gigabyte.cn/Graphics-Card/{row['技嘉规格型号copy']}" target="_blank">
                        <img src="https://irx999.fun/file/test_Image.png" style="max-width:{set_image_width}%;">
                    </a>
                    """, unsafe_allow_html=True)
            column_config_setting = {
                "Image": st.column_config.ImageColumn(
                    "图片",
                    width="medium",
                )
            }

            st.dataframe(display_data.drop(columns= ["技嘉规格型号copy"],),
                        use_container_width= True,

                        column_config= column_config_setting )
        else:
            st.title("请选择要对比的显卡型号")
