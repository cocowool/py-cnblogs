from blog2markdown import html2markdown
from blog2markdown import blog2html
# import html5lib

# h = html5lib.HTMLParser(tree=html5lib.getTreeBuilder("dom"))
# s = h.parse('<div><h1>hello world</h1><table><tr><td>xxxxx</td></tr></table></div>').toxml()
# print(s)

h2m = html2markdown()
# print( h2m.feed('<div><h1>hello world</h1><table><tr><td>xxxxx</td></tr></table></div>') )

# md_result = h2m.convert('<div><h1><a href="http://www.baidu.com">hello</a> world</h1><ul><li><a href="www.baidu.com">AAAAAAA</a></li><li><a href="sina.com">sina.com</a></ul><br /><em>xx</em><p>today is a very <strong>xxxx</strong> day</p><table><th><td>Header</td><td>yyyy</td></th><tr><td>xxxxx</td><td>ccccc</td></tr></table></div>')
# # md_result = h2m.convert('<div><h1>hello world</h1><br /><em>xx</em><p>today is a very <strong>xxxx</strong> day</p><table><th><td>Header</td><td>yyyy</td></th><tr><td>xxxxx</td><td>ccccc</td></tr></table></div>')
# print("========= Convert Result ==========")
# print(md_result)

# md = h2m.convertFile('/Users/shiqiang/Projects/py-cnblogs/cnblogs/htmls/2020-03-16-hexo-image-link.html')
# print(md)

# 示例
# 
b2h = blog2html()
# b2h.get_cnblogs('https://www.cnblogs.com/cocowool/')
b2h.get_all_posts('https://www.cnblogs.com/cocowool/archive/2012/01/17/macvpn.html')


# 测试Tag替换
# from bs4 import BeautifulSoup
# markup = '<ul><li><img src="./a.jpg" /></li><li><img src="./b.jpg" /></li></ul>'
# soup = BeautifulSoup(markup, 'html.parser')
# a_tag = soup.find_all('img')


# for i in a_tag:
#     new_tag = soup.new_tag("img")
#     new_tag['src'] = "example.net"
#     i.replace_with(new_tag)

# print(soup)