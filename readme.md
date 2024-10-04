# 这个仓库主要实现某些产品的参数对比， 
  ## 使用streamlit 做页面展示





# 待开发
  1. 宽度高度设定
  2. CPU参数对比, 主要以AMD 为主
  3. 主板参数对比, 主要以技嘉为主



# docker 部署
```yaml
version: '3'
services:
  productchnfohub :
    container_name: productchnfohub
    build: .
    ports:
    - "8501:8501"
    volumes:
    - ./models:/src/models
```



if "*" in c_goods_sku:
            c_goods_sku = c_goods_sku[:-2]


        return_list = {}
        for  k , v  in [["正常",c_goods_sku],
                        ["**",c_goods_sku+"**"],
                        ["*!",c_goods_sku+"*!"],
                        ["*?",c_goods_sku+"*?"]]:
