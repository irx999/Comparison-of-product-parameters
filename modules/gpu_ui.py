'''GPU 产品参数对比工具'''

import pandas as pd
import streamlit as st


def gpu_product_parameters_comparison(df: pd.DataFrame =None):
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
            display_data = df[[gpu_column] + selected_params \
                            + ["技嘉规格型号copy"]+["Image"]].set_index(gpu_column)
        else:
            display_data = df.set_index(gpu_column)


        if selected_gpus:

            st.title("竖向表格  参数对比")
            cols = st.columns([ 1.1 if len(selected_gpus)>= 10 else \
                                1.0 if len(selected_gpus)>= 6 else \
                                0.6 if len(selected_gpus)>= 3 else \
                                0.5 if len(selected_gpus)> 1 else 0.4]  \
                                + [1] * len(selected_gpus))
            with cols[0]:
                st.write("显卡图片：")
            for index, row in display_data.iterrows():
                with cols[selected_gpus.index(index) + 1]:
                    set_image_width = 100 if len(selected_gpus) > 3 else 40
                    st.markdown(f"""
                    <div style="text-align: center;">
                    <a href="http://w.irx999.fun:23333/_uploads/显卡图片/{row['技嘉规格型号copy']}/{row['技嘉规格型号copy']}显卡图片.png" target="_blank">
                    <img src="http://w.irx999.fun:23333/_uploads/显卡图片/{row['技嘉规格型号copy']}/{row['技嘉规格型号copy']}显卡图片.png" style="max-width:{set_image_width}%;">
                    </a>
                    </div>
                    <div style="text-align: center; margin-top: 1px; border:  None; padding: 0px;">
                    <a href="https://www.gigabyte.cn/Graphics-Card/{row['技嘉规格型号copy']}" target="_blank">
                    <button style="border: none;">{row["技嘉规格型号copy"]}特色重点</button>
                    </a>
                    """, unsafe_allow_html=True)

            #st.title("")

            column_config_setting = {k: st.column_config.Column(k, width="small") for k in selected_gpus}
            
            st.dataframe(display_data.drop(columns= ["技嘉规格型号copy","Image"]).T,
                        use_container_width= True,
                        column_config=column_config_setting,height=1020)

            st.title("竖向表格  参数对比")
            column_config_setting = {
                "Image": st.column_config.ImageColumn(
                    "图片",
                    width="small",
                )
            }
            st.dataframe(display_data,
                         use_container_width= True,
                         column_config= column_config_setting )



        else:
            st.markdown("<h1 style='text-align: center;'> -- 请选择的对比的显卡型号 --</h1>",\
                         unsafe_allow_html=True)
