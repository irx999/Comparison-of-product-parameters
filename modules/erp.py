import requests
COMPANY_DOMAIN = ""

class ERP():
    """ 这里是3cerp功能相关的类 """
    def __init__(self,erpcookies=None) -> None:
        self.cookies = {'3cu':erpcookies}
        self.headers = {"Accept-Encoding":"gzip, deflate","User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}

    def get_product_list(self,cBillcode):
        """ 获取产品列表 """
        need_key = ["c_goods_sku","c_product_goods_name","n"]
        url = f"http://{COMPANY_DOMAIN}/pages/net/searchNetOrderDetail.htm?cBillcode={cBillcode}"
        res = requests.get(url=url,headers=self.headers,cookies=self.cookies,verify= False,timeout= 20)
        data = res.json()["data"]
        return {"emp_name":data["data_order"][0]["c_handing_emp_org_name"], "data":[{key: d[key] for key in need_key} for d in data["data_order_deliver_goods"]]}
    
    def get_product_detail(self,c_goods_sku):
        """ 直接从分区库存里面获取可销数 """

        need_key  = ["c_c_name","n_stock","n_stock_able"]
        if "*" in c_goods_sku:
            c_goods_sku = c_goods_sku[:-2]


        return_list = {}
        for  k , v  in [["正常",c_goods_sku],
                        ["**",c_goods_sku+"**"],
                        ["*!",c_goods_sku+"*!"],
                        ["*?",c_goods_sku+"*?"]]:
            
            if "*" not in c_goods_sku or  "*" not in k:
                url = f"http://{COMPANY_DOMAIN}/pages/stock/searchDeoptStockList.htm?filter={v}&depotIds=&b_stock=0&search_category=&search_out_stock=0&pageSize=100&pageIndex=0&sortField=&sortOrder="
                res = requests.get(url=url,headers=self.headers,cookies=self.cookies,verify= False,timeout= 20)

                if res.json()["total"] == 0:
                    return_list[k] = ["无此产品"]
                else:
                    good_list = res.json()["data"]
                    extracted_data = [{key: d[key] for key in need_key} for d in good_list]
                    return_list[k] = extracted_data
        return return_list


erp = ERP(erpcookies="")
def main(cBillcode):
    """ 启动函数 """
    data = erp.get_product_list(cBillcode)


    for goods in data["data"]:
        goods["test"] = erp.get_product_detail(goods["c_goods_sku"])

    return 
