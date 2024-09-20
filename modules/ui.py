'''这里是写UI页面相关'''
import streamlit as st
import pandas as pd



# 导入数据加载模块
from modules.load_data import GPU_DATA,MB_DATA
# 导入CPU参数对比模块
from modules.gpu_ui import gpu_product_parameters_comparison
from modules.mb_ui import mb_product_parameters_comparison




def main_ui():
    """主页面"""
    params = st.query_params
    current_page  = params.get("page", "欢迎页")

    #print(current_page,"当前页面")

    def navigate_to(page):
        params["page"] = page
        #main_ui()

    pagesetting = {">> 1. 欢迎页": "欢迎页",
                   ">> 2. CPU参数对比工具- 待开发": "CPU参数对比工具",
                   ">> 3. 主板参数对比工具": "主板参数对比工具",
                   ">> 4. 显卡参数对比工具": "显卡参数对比工具",
                   #">> 5. 测试页面": "测试页面",
    }
    for   page_name, page_id in pagesetting.items():
        st.sidebar.button(page_name, on_click=navigate_to, args=(page_id,))

    # 根据当前页面显示内容
    match current_page:
        case "欢迎页":
            welcome_page()

        case "CPU参数对比工具":
            cpu_product_parameters_comparison()

        case "主板参数对比工具":
            mb_product_parameters_comparison(MB_DATA)

        case "显卡参数对比工具":
            gpu_product_parameters_comparison(GPU_DATA)

        case "测试页面":
            test_page()

        case _:  # 其他页面
            st.markdown("<h1 style='text-align: center;'>-- 页面不存在 --</h1>", unsafe_allow_html=True)

def test_page(test_data:pd.DataFrame = None):
    """测试页面"""
    if not test_data.empty:
        st.title("测试页面")
        match st.selectbox("选择观测维度", ["店铺负责人", "店铺", "业务员"], index=0):
            case "店铺负责人":
                test_data["日期"] = pd.to_datetime(test_data["出库日期"]).dt.date
                test_data = test_data.groupby(["日期","店铺负责人"])\
                    .agg({'销售额': 'sum',"整机数量":"sum"}).reset_index()
                st.dataframe(test_data)
                st.line_chart(test_data,x="日期",y=["整机数量"],color="店铺负责人",use_container_width = True)
            case _:
                st.write("123")
    else:
        st.markdown("<h1 style='text-align: center;'>-- 无测试数据 --</h1>", unsafe_allow_html=True)
def welcome_page():
    """欢迎页"""
    st.markdown("<h1 style='text-align: center;'>欢迎使用参数对比工具</h1>", unsafe_allow_html=True)



def cpu_product_parameters_comparison(df: pd.DataFrame =None):
    """ CPU参数页面 """
    st.markdown("<h1 style='text-align: center;'>CPU参数对比工具- 待开发</h1>",
                         unsafe_allow_html=True)
