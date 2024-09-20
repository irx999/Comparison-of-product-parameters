'''主板产品参数对比工具'''

import pandas as pd
import streamlit as st



def mb_product_parameters_comparison(df: pd.DataFrame =None):
    '''主板产品参数对比工具'''
    st.title('主板产品参数对比工具')
    if  df is not None :

        所有列名 = df.columns.tolist()
        # 创建一个列表，用于存放需筛选的东西
        col0, col1, col2 = st.columns(3)

        with col0:
            选择阵营  = st.selectbox('选择阵营',["全部","Intel","amd",], index=0)
            if 选择阵营 == "Intel":
                df = df[df["阵营"] == "Intel"]
            elif 选择阵营 == "AMD":
                df = df[df["阵营"] == "AMD"]
        with col1:
            选择查看的列 = st.selectbox("选择查看的列", ["简称", "名称", "技嘉规格型号"], index=0)
        with col2:
            筛选框 = st.selectbox("选择筛选项", ["芯片组", "系列"], index=0)

        筛选项目 = df[筛选框].unique().tolist()
        col1, col2 = st.columns(2)
        with col1:
            筛选条件 = st.multiselect(f"选择筛选{筛选框}", 筛选项目, default=筛选项目[:3])

        if 筛选条件:
            df = df[df[筛选框].isin(筛选条件)]

        mb_options = df[选择查看的列].unique().tolist()
        parameter_options = [col for col in 所有列名 if col != 选择查看的列]
        with col2:
            # 去除显卡型号列，剩余的是参数列
            选择查看的参数 = st.multiselect("选择参数进行对比（如果不选，默认展示所有参数)",
                                             parameter_options,
                                             default=None
                                             )

        选择的型号 = st.multiselect("选择要对比的显卡型号",
                                       mb_options,
                                       default=mb_options[:10])


        if 选择的型号:
            df = df[df[选择查看的列].isin(选择的型号)]
            df["技嘉规格型号copy"] = df["技嘉规格型号"]
            st.write(f"显示型号：{选择查看的列}")
            st.write(f"展示的参数：{', '.join(选择查看的参数) if 选择查看的参数 else '所有参数'}")

            
            if 选择查看的参数:
                display_data = df[[选择查看的列] + 选择查看的参数 \
                                + ["技嘉规格型号copy"]].set_index(选择查看的列)
            else:
                display_data = df.set_index(选择查看的列)

            st.title("竖向表格  参数对比")
            cols = st.columns([ 1.1 if len(选择的型号)>= 10 else \
                                1.0 if len(选择的型号)>= 6 else \
                                0.6 if len(选择的型号)>= 3 else \
                                0.5 if len(选择的型号)> 1 else 0.4]  \
                                + [1] * len(选择的型号))
            with cols[0]:
                st.write("显卡图片：")
            for index, row in display_data.iterrows():
                with cols[选择的型号.index(index) + 1]:
                    set_image_width = 100 if len(选择的型号) > 3 else 40
                    st.markdown(f"""
                    <div style="text-align: center;">
                    <a href="{row["盒子图片"]}""= target="_blank">
                    <img src="{row["盒子图片"]}" style="max-width:{set_image_width}%;">
                    <a href="{row["接口图片"]}" target="_blank">
                    <img src="{row["接口图片"]}" style="max-width:{set_image_width}%;">
                    </a>
                    </div>
                    <div style="text-align: center; margin-top: 1px; border:  None; padding: 0px;">
                    <a href="https://www.gigabyte.cn/Motherboard/{row['技嘉规格型号copy']}" target="_blank">
                    <button style="border: none;">{row["技嘉规格型号copy"]}特色重点</button>
                    </a>
                    """, unsafe_allow_html=True)

            #st.title("")

            column_config_setting = {k: st.column_config.Column(k, width="small") for k in 选择的型号}

            st.dataframe(display_data.drop(columns= ["技嘉规格型号copy"]).T,
                        use_container_width= True,
                        column_config=column_config_setting,height=500)

            st.title("竖向表格  参数对比")
            column_config_setting = {
                "盒子图片": st.column_config.ImageColumn(
                    "盒子图片",
                    width="small",
                ),
                "正面图片": st.column_config.ImageColumn(
                    "正面图片",
                    width="small",
                )
            }
            st.dataframe(display_data,
                         use_container_width= True,
                         column_config= column_config_setting )



        else:
            st.markdown("<h1 style='text-align: center;'> -- 请选择的对比的主板型号 --</h1>",\
                         unsafe_allow_html=True)









    else:
        st.markdown("<h1 style='text-align: center;'> -- 数据加载错误,请联系管理员 --</h1>",\
                         unsafe_allow_html=True)
