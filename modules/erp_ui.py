""" erp功能相关 """
import streamlit as st
from modules.erp import main




def test_page():
    """ 测试页面 """

    def test_func():       
        st.session_state.data_list = main(input_text)



    input_text = st.text_input("请输入测试文本")
    st.button("测试按钮",on_click=test_func)

    st.title("产品库存信息展示")

    # 遍历每个商品并展示
    if 'data_list' in st.session_state:

        st.title(f"产品库存信息展示{st.session_state.data_list['emp_name']}")
        for product in st.session_state.data_list["data"]:
            col1, col2 = st.columns(2)
            with col1:
                标题1 ,标题2 = st.columns(2)
                with 标题1:
                    st.button(f"商品名称: {product['c_product_goods_name']}")
                with 标题2:
                    st.button(f"开单数量: {int(product['n'])}",key=product['c_goods_sku'])


            with col2:


                def show_product_info(product,product_label):
                    st.write(f"<<{product_label}>>")
                    if product['test'][product_label] == ['无此产品']:
                        st.write("无此产品")
                    else:
                        for info in product['test'][product_label]:
                            库存可用 =   info['n_stock_able'] if info['n_stock_able'] else 0
                            st.write(f"{info['c_c_name']}--->库存: {int(info['n_stock'])}, 可销: {库存可用}")


                label1 , label2 ,label3,label4,= st.columns(4)
                with label1:
                    show_product_info(product,"正常")
                with label2:
                    show_product_info(product,"**")
                with label3:
                    show_product_info(product,"*!")
                with label4:
                    show_product_info(product,"*?")


        # 可以选择用st.json展示原始数据
        st.subheader("原始数据")
        st.json(st.session_state.data_list)
