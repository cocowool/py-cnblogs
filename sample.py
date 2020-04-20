from blog2markdown import html2markdown
from blog2markdown import blog2html

# 将博客文章和博客用到的图片保存到本地，文章保存为html格式，图片保存到markdown文件夹下
# 输入博客的入口，则自动将所有博客文章下载到本地的 cnblogs-{blog-name}/html 文件夹下
b2h = blog2html()
b2h.get_cnblogs('https://www.cnblogs.com/ityouknow/')

h2m = html2markdown()
# Conver Folder
# 将文件夹下的html文件批量转换为markdown文件
# h2m.convertFolder('/Users/shiqiang/Projects/py-cnblogs/cnblogs-coco1s/htmls', '/Users/shiqiang/Projects/py-cnblogs/cnblogs-coco1s/markdowns')