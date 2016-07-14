# fetch_baidu_index

目的：本项目主要是用来抓取百度指数的值。因为百度指数为了防止抓取，将数字转成了图片。

# 运行步骤:
1.修改baidu_index/config.py要启用的浏览器driver, 因为有些人PhantomJS配置可能有问题，默认使用Firefox(容易配置).
  具体参考selenium的浏览器环境配置

2.修改baidu_index/config.py里面的百度账号跟密码

3.baidu_index/config.py 不配置start_date和end_date，可以查询到这个关键词数据的最大区间

4. python main.py

