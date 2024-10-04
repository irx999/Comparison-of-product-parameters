# 这个仓库主要实现某些产品的参数对比， 
  ## 使用streamlit 做页面展示





# 待开发
  1. 登录验证框
  2. 空值判断
  3. 表格展示
  4. redis删除多余的字段
  5. 



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
