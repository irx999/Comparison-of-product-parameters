"""数据加载模块"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine



# def decode_bytes(val):
#     '''
#     非常核心的一个代码, 这里会讲将mysql 的返回的重新编码一下,不然就是乱码的
    
#     script =
#         mysql ->  dataframe.map(decode_bytes)
#     '''
#     if isinstance(val, str):
#         try:
#             return val.encode('latin1').decode('gbk')
#         except ValueError:
#             return val
#     return val
# @st.cache_data
# def get_sql_to_df_bytime(table_name,select_columns,start_time,end_time) -> pd.DataFrame:
#     ''' 获取mssql数据库表指定时间范围内的数据'''
#     db_string  =  st.secrets["MSSQL_database"]["DB_STRING"]
#     sql=f"SELECT * FROM {table_name} WHERE\
#             {select_columns} > '{start_time}' and {select_columns} < '{end_time}'"
#     data = pd.read_sql(sql,con=create_engine(db_string))
#     return data.map(decode_bytes)


# zj = get_sql_to_df_bytime('单据利润', '出库日期','2024-09-01 00:00:00', '2024-09-15 00:00:00')\
#         .loc[:,['出库日期','店铺负责人','店铺',"业务员","是否整机",'整机数量','销售额','净利润']]
# zj = zj.loc[zj["是否整机"] == "整机销售"]
# TEST_DATA = zj

@st.cache_data
def load_data(excel_file:str, sheet_name:str) -> pd.DataFrame:
    """excel文件数据加载"""
    def  characterConversion(val):
        """ 字符转换 """
        try:
            return int(val)
        except ValueError:
            return str(val)


    return pd.read_excel(excel_file, sheet_name=sheet_name).map(characterConversion)



GPU_DATA = load_data('./modules/product_data.xlsx', 'GPU')
MB_DATA = load_data('./modules/product_data.xlsx', 'MB')

if __name__ == '__main__':
    print(st.secrets["MSSQL_database"]["DB_STRING"])
    #print(TEST_DATA)
