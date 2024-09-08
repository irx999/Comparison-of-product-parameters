
import streamlit as st
import pandas as pd

def product_parameters_comparison(df):
    # 页面标题
    st.title('显卡参数对比工具')

    if not df.empty:
        # 提取所有列名作为选项
        column_options = df.columns.tolist()

        #创建一个列表，用于存放需筛选的东西
        col0 , col1, col2 = st.columns(3)
        with  col0:
            是否在售  = st.selectbox("是否显示所有显卡型号", ["在售","已停售","全部"])
            if  是否在售  == "在售":
                df = df[df["是否在售"] == "在售"]
            elif  是否在售  == "已停售":
                df = df[df["是否在售"] == "not_sale"]
        with  col1:
            gpu_column = st.selectbox("选择显卡型号所在的列", ["简称","技嘉官网名称","技嘉规格型号"], index=0)
        with  col2:
            筛选框  = st.selectbox("选择筛选项目",["芯片组","阵营","系列"],index=0)

        筛选项目 = df[筛选框].unique().tolist()

        col1 ,col2 = st.columns(2)
        with  col1:
            筛选条件 = st.multiselect(f"选择筛选{筛选框}",筛选项目,default=筛选项目[:3])

        if 筛选条件:
            df = df[df[筛选框].isin(筛选条件)]

        # 选择显卡型号列后，从该列中选择具体的显卡型号
        gpu_options = df[gpu_column].unique().tolist()
        parameter_options = [col for col in column_options if col != gpu_column]
        with  col2:
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



        # 让用户选择参数，默认选择所有参数


        # 根据用户选择展示数据
        st.write(f"显卡型号：{gpu_column}")
        st.write(f"展示的参数：{', '.join(selected_params) if selected_params else '所有参数'}")

        # 构建展示数据的 DataFrame，行是显卡型号，列是选中的参数
        if selected_params:
            display_data = df[[gpu_column] + selected_params].set_index(gpu_column)
        else:
            display_data = df.set_index(gpu_column)

        # 展示最终的对比表格
        st.write("参数对比表：")
        st.dataframe(display_data.T,use_container_width= (len(selected_gpus) > 3))
