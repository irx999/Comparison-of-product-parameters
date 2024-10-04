""" erp功能相关 """
import streamlit as st
from modules.erp import erp
import logging



logging.basicConfig(filename='app.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

    


def test_page():
    """ 测试页面 """
    user_input = st.text_input("请输入密码:", type="password")
    PASSWORD = "123"
    if user_input == PASSWORD:
        st.success("欢迎进入ERP功能页面！")
        # 在这里添加你的ERP功能相关代码

        def test_func():

            datalist   = erp.get_product_list(input_text)
            data = erp.get_product_detail(datalist["data"])


            st.session_state.update_time = erp.update_time
            st.session_state.empname  = datalist['emp_name']
            st.session_state.data_list = data

        st.title(f"上次数据库更新时间:{erp.update_time}",)
        input_text = st.text_input("请输入订单编号")
        st.button("检测按钮",on_click=test_func)
        # 遍历每个商品并展示
        if 'data_list' in st.session_state:
            col1, col2 = st.columns(2)
            with col1:
                st.title(f"{st.session_state.empname}" )
            with col2:
                label1, label2 ,label3,label4,= st.columns(4)
                with label1:
                    st.title("<正常>")
                with label2:
                    st.title("<**>")
                with label3:
                    st.title("<*!>")
                with label4:
                    st.title("<*?>")


            for product in st.session_state.data_list.values():
                col1, col2 = st.columns(2)
                with col1:
                    标题1 ,标题2 = st.columns(2)
                    with 标题1:
                        st.write(f"{product['c_product_goods_name']}")
                    with 标题2:
                        st.write(f"{int(product['n'])}",)

                    for lable in  ["**","*!","*?"]:
                        if lable in product:
                            for item in product[lable]:
                                if item['分区名称'] == '公司大库':
                                    可销数 = item['分区可销']
                                    # 找到后结束循环

                                    if '*' not in product['c_product_goods_name'] and  可销数 >0 and input_text is not None:
                                        st.warning(f"{lable} 可销数量: {int(可销数)}",icon="⚠️")
                                        logging.info(f"{st.session_state.empname,input_text,product['c_product_goods_name']}")

                                    break
                with col2:
                    def show_product_info(product,product_label):
                        #st.write(f"<<{product_label}>>")
                        if product_label not in product:
                            st.write("无此产品")
                        else:
                            for info in product[product_label]:
                                库存可用 =   int(info['分区可销']) if info['分区可销'] else 0
                                st.write(f"{info['分区名称']}--->库存: {int(info['分区库存'])}, 可销: {库存可用}")

                        #if '**' not in product and :
                    label1 , label2 ,label3,label4,= st.columns(4)
                    with label1:
                        show_product_info(product,"正常")
                    with label2:
                        show_product_info(product,"**")
                    with label3:
                        show_product_info(product,"*!")
                    with label4:
                        show_product_info(product,"*?")

                st.write("---------------------------------------------------------------------------------------------------------------------- ")


        # 可以选择用st.json展示原始数据
        # st.subheader("原始数据")
        # st.json(st.session_state.data_list)


    elif user_input == "321":
        st.warning("日志记录:")
        try:
            with open('app.log', 'r') as file:
                log_contents = file.read()
                st.text_area("日志内容", log_contents, height=300)
        except FileNotFoundError:
            st.warning("日志文件不存在。")

    else:
        st.warning("密码错误，请重试！")
