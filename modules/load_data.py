"""数据加载模块"""

from re import M
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymssql




def decode_bytes(val):
    '''
    非常核心的一个代码, 这里会讲将mysql 的返回的重新编码一下,不然就是乱码的
    
    script =
        mysql ->  dataframe.map(decode_bytes)
    '''
    if isinstance(val, str):
        try:
            return val.encode('latin1').decode('gbk')
        except:
            return val
    return val












@st.cache_data
def load_data(excel_file:str, sheet_name:str) -> pd.DataFrame:
    """excel文件数据加载"""
    return pd.read_excel(excel_file, sheet_name=sheet_name)


@st.cache_data(ttl=600)
def get_sql_to_df_bytime(table_name,开始时间,结束时间,select_columns) -> pd.DataFrame:
    '''
    获取mssql数据库表指定时间范围内的数据
    '''
    DB_STRING = f"mssql+pymssql://{st.secrets["MSSQL_database"]["username"]}:{st.secrets["MSSQL_database"]["password"]}@{st.secrets["MSSQL_database"]["server"]}:{st.secrets["MSSQL_database"]["port"]}/{st.secrets["MSSQL_database"]["database"]}?charset=utf8"
    # conn = pymssql.connect(server= st.secrets["MSSQL_database"]["server"],
    #                             database=st.secrets["MSSQL_database"]["database"],
    #                             user=st.secrets["MSSQL_database"]["username"],
    #                             password=st.secrets["MSSQL_database"]["password"],
    #                             port=st.secrets["MSSQL_database"]["port"])


    engine = create_engine(DB_STRING)
    sql=f"SELECT * FROM {table_name} WHERE\
            {select_columns} > '{开始时间}' and {select_columns} < '{结束时间}'"
    data = pd.read_sql(sql,con=engine)
    data = data.map(decode_bytes)
    return data



TEST_DATA = get_sql_to_df_bytime('单据利润', '2024-09-14 00:00:00', '2024-09-15 00:00:00', '出库日期')
GPU_DATA = load_data('./modules/product_data.xlsx', 'GPU')


if __name__ == '__main__':
    print(st.secrets["MSSQL_database"]["server"])
    print(TEST_DATA)
