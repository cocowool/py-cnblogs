# py-cnblogs 抓取博客园文章并保存为Markdown

> 本项目目标有两个：
> 1. 抓取自己的博客园文章，并持久化保存。
> 2. 将本地文件转换为Hexo所用的Mardown 格式。

## 用法


## 几个现有框架的对比
* [html2markdown](https://github.com/dlon/html2markdown)：无法对整段的HTML进行解析，不支持table的解析和转换
* [h2md](https://github.com/canovie/h2md)：能够解析整段的HTML，不支持table


## 修改记录
* [2020-03-30] 创建 blog2markdown 的包，将相关操作都封装到包中
* [2020-03-16] 将Scrapy方式改为requests方式

## 参考资料
1. [Python3用requests保存网页](https://www.cnblogs.com/nancyzhu/p/8412950.html)
2. [html2markdown](https://github.com/kevinywb/html2markdown)
3. [BeautifulSoup Document](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id20)
4. [请问python怎么判断库是否已安装？](https://www.zhihu.com/question/329900077/answer/738996774)
5. [Python3 html.parser](https://docs.python.org/3.7/library/html.parser.html?highlight=html.parser#module-html.parser)
6. [Github html.parser.HTMLParser](https://github.com/python/cpython/blob/3.7/Lib/html/parser.py)
