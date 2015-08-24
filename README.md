Adding feature of price compare in USA with the popular shopping websites

一个简单的在线比价搜索站点
=============

1. 安装环境
--------------

要编译并运行这个网站，你需要

- django-1.5.1
- python-2.7
- BeautifulSoup 3 (http://www.crummy.com/software/BeautifulSoup/)

> 注意：
>
> 1. 在`PriceCompare/settings.py`中， 设置 `DEBUG=True` 以便使用
>
>   `python manage.py runserver`
>
>	进行快速测试
>
> 2. 请先建立数据库文件：
>
>   `python manage.py syncdb`


`Makefile` 文件用于创建epydoc, 你可以自行重新生成文档，只要你安装了epydoc。否则你需要：

    `pip install epydoc`

或从http://epydoc.sourceforge.net上下载



