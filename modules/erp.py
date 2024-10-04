""" erp功能相关的类 """
import requests
import redis
import streamlit as st
import datetime
import json
from math import ceil
import pytz


#基础信息配置
COMPANY_DOMAIN  = st.secrets["ERP"]["COMPANY_DOMAIN"]
erpcookies = st.secrets["ERP"]["erpcookies"]
r = redis.Redis(host='redis_container', port=6379, db=0)

class ERP():
    """ 这里是3cerp功能相关的类 """
    def __init__(self,erpcookies=None) -> None:
        self.cookies = {'3cu':erpcookies}
        self.headers = {"Accept-Encoding":"gzip, deflate","User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
        self.update_time = r.get("update_time:update_time")
    def get_product_list(self,cBillcode):
        """ 获取产品列表 """
        if not cBillcode.startswith("NO-"):
            url  = f"http://{COMPANY_DOMAIN}/pages/net/getNetOrderList.htm?totalCount=1&search_billcode_filter={cBillcode}&search_billcode_key=platformNo"
            res = requests.get(url=url,headers=self.headers,cookies=self.cookies,verify= False,timeout= 20)
            cBillcode = res.json()["data"][0]["c_billcode"]


        need_key = ["c_goods_sku","c_product_goods_name","n"]
        url = f"http://{COMPANY_DOMAIN}/pages/net/searchNetOrderDetail.htm?cBillcode={cBillcode}"
        res = requests.get(url=url,headers=self.headers,cookies=self.cookies,verify= False,timeout= 20)
        data = res.json()["data"]
        return {"emp_name":data["data_order"][0]["c_handing_emp_org_name"], "data":[{key: d[key] for key in need_key} for d in data["data_order_deliver_goods"]]}
    


    def get_product_detail(self,input_data: list) -> dict:
        """ 这里是获取产品详情的函数 """


        input_data = {d["c_goods_sku"]:d for d in input_data}

        
        if not r.get("update_time:update_time"):

            self.update_erp_data_to_redis()
            self.update_time = r.get("update_time:update_time")
        for c_goods_sku  in input_data.keys():
                
                if "*" in c_goods_sku:
                    goods_sku = c_goods_sku[:-2]
                else:
                    goods_sku = c_goods_sku


            
                for  k , v  in [["正常",goods_sku],
                                ["**",goods_sku+"**"],
                                ["*!",goods_sku+"*!"],
                                ["*?",goods_sku+"*?"]]:
                    
                #获取redis数据
                    redis_data = r.get(f"erp:{v}")
                    if redis_data:
                        redis_data = json.loads(redis_data)
                        #print(redis_data)
                        input_data[c_goods_sku][k] = redis_data

                    else:
                        pass

        return input_data

    def  update_erp_data_to_redis(self,):
        """ 更新erp数据到redis """
        total = 2000
        pageindex  = 0
        while pageindex < ceil(total / 2000)  :

            url = f"http://{COMPANY_DOMAIN}/pages/stock/searchDeoptStockList.htm?filter=&depotIds=&b_stock=0&search_category=&search_out_stock=0&pageSize=2000&pageIndex={pageindex}&sortField=&sortOrder="
            res = requests.get(url=url,headers=self.headers,cookies=self.cookies,verify= False,timeout= 20)
            if pageindex == 0 :
                dict_sum = res.json()["data"]
                total = res.json()["total"]
            else:
                dict_sum +=res.json()["data"]
            pageindex +=1


        input_data = {}
        for item in dict_sum:
            sku = item["b_c_sku"]
            if sku not in input_data:
                input_data[sku] = [{
                    "商品名称": sku,
                    "分区名称": item["c_c_name"],
                    "分区库存": item["n_stock"],
                    "分区可销": item["n_stock_able"]
                }]
            else:
                # 如果已经存在，则追加
                input_data[sku] += [{
                    "商品名称": sku,
                    "分区名称": item["c_c_name"],
                    "分区库存": item["n_stock"],
                    "分区可销": item["n_stock_able"]
                }]
        # 将合并后的数据存储到 Redis 中

        r.set("update_time:update_time", str(datetime.datetime.now(pytz.timezone('Asia/Shanghai'))))

        r.expire("update_time:update_time", 300)
        for key, value in input_data.items():
            r.set(f"erp:{key}", json.dumps(value, ensure_ascii=False))
            r.expire(f"erp:{key}", 300)







erp = ERP(erpcookies=st.secrets["ERP"]["erpcookies"])


if __name__ == '__main__':


    data = erp.get_product_list("NO-241003-0071631")

    #erp.update_erp_data_to_redis()

    erp.get_product_detail(data["data"])

