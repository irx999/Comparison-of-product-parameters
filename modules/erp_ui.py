""" erp功能相关 """
import streamlit as st
from modules.erp import erp
import pandas as pd
import logging



logging.basicConfig(filename='modules/app.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


def erp_ui():
    """ 测试页面 """
    st.warning(f"上次数据库更新时间:{str(erp.update_time)[2:18]}",)
    
    col1, col2 = st.columns(2)
    with col1:
        input_text = st.text_input("请输入订单编号")
        
    with col2:
        def test_func():
            #点击on_click事件，更新数据库
            if input_text  == "":
                st.error("请输入订单编号！")
            else:
                abc = input_text.replace(" ","")
                print(abc)
                try:
                    datalist   = erp.get_product_list(abc)
                    data = erp.get_product_detail(datalist["data"])
                    st.session_state.update_time = erp.update_time
                    st.session_state.empname  = datalist['emp_name']
                    st.session_state.data_list = data
                except ValueError:
                    st.error("订单编号准确！")
                except:
                    st.error("订单编号不存在！")
                finally:
                    st.rerun()

    
    st.button("检测按钮",on_click=test_func)
    # 遍历每个商品并展示
    if 'data_list' in st.session_state:
        df = pd.DataFrame(st.session_state.data_list)
        
        df.rename(columns={'c_product_goods_name': '商品名称',"n":"开单数量"}, inplace=True)

        def check_conditions(row):
            if '*' not in row['商品名称'] and row['**'] > 0:
                return '❌'
            else:
                return '✅'

        
        df['Z'] = df.apply(check_conditions, axis=1)
        
        df.insert(0, '校验结果', df['Z'])
        df.drop(columns=['c_goods_sku',"Z"],inplace=True)
        logging.info(f"用户{st.session_state.empname}查询了订单{input_text}的商品信息。{ df[df['校验结果'] == '✅'].to_dict()}")


        column_config = {
            '商品名称': {'width': 300},
            '开单数量': {'width': 20},
            '校验结果': {'width': 20}}
        #df= df.reset_index(drop=True, inplace=True)
        st.dataframe(df,use_container_width= True,height=800,
                    column_config = column_config )


    passpd  = st.text_input("请输入日志查看密码")
    if passpd == "123":
        st.warning("日志记录:")
        try:
            with open('modules/app.log', 'r') as file:
                log_contents = file.read()
                st.text_area("日志内容", log_contents, height=300)
        except FileNotFoundError:
            st.warning("日志文件不存在。")
    elif  passpd != "":
        st.warning("密码错误，请重试！")
