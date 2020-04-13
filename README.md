# py-cnblogs 抓取博客园文章并保存为 Markdown 格式文档

> 本项目目标：抓取自己的博客园文章，转换为 Hexo 所用的Mardown格式，并且持久化保存。

## 用法


```python

```

## 几个现有框架的对比
* [html2markdown](https://github.com/dlon/html2markdown)：无法对整段的HTML进行解析，不支持table的解析和转换
* [h2md](https://github.com/canovie/h2md)：能够解析整段的HTML，不支持table


## 修改记录
* [2020-04-13] 完善了支持的元素，完善了生成md的格式
* [2020-04-09] 最近几天调整了下递归方法，支持了 table\a\ul\li 等元素
* [2020-03-30] 创建 blog2markdown 的包，将相关操作都封装到包中
* [2020-03-16] 将Scrapy方式改为requests方式

## 参考资料
1. [Python3用requests保存网页](https://www.cnblogs.com/nancyzhu/p/8412950.html)
2. [html2markdown](https://github.com/kevinywb/html2markdown)
3. [BeautifulSoup Document](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id20)
4. [请问python怎么判断库是否已安装？](https://www.zhihu.com/question/329900077/answer/738996774)
5. [Python3 html.parser](https://docs.python.org/3.7/library/html.parser.html?highlight=html.parser#module-html.parser)
6. [Github html.parser.HTMLParser](https://github.com/python/cpython/blob/3.7/Lib/html/parser.py)
7. [Python使用urllib库、requests库下载图片的方法比较](https://baijiahao.baidu.com/s?id=1630594345004620959&wfr=spider&for=pc)
8. [python 遍历文件夹下的所有文件](https://www.cnblogs.com/wt7018/p/11610286.html)
9. [神奇的不可见空格<200b>导致代码异常](https://www.cnblogs.com/ichochy/p/11592881.html)
