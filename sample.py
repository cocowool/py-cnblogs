from blog2markdown import html2markdown
from blog2markdown import blog2html
# import html5lib

# h = html5lib.HTMLParser(tree=html5lib.getTreeBuilder("dom"))
# s = h.parse('<div><h1>hello world</h1><table><tr><td>xxxxx</td></tr></table></div>').toxml()
# print(s)

h2m = html2markdown()
# print( h2m.feed('<div><h1>hello world</h1><table><tr><td>xxxxx</td></tr></table></div>') )
md_result = h2m.convert('<div><h1>hello world</h1><br /><em>xx</em><p>today is a very <strong>xxxx</strong> day</p><table><th><td>Header</td><td>yyyy</td></th><tr><td>xxxxx</td><td>ccccc</td></tr></table></div>')
print("========= Convert Result ==========")
print(md_result)

# md = h2m.convertFile('/Users/shiqiang/Projects/py-cnblogs/cnblogs/htmls/2020-03-29-google_adsense_no_slog_size_error.html')
# print(md)

# 示例
# 
# b2h = blog2html()
# b2h.get_all_posts('https://www.cnblogs.com/cocowool/p/google_adsense_no_slog_size_error.html')