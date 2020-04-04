from blog2markdown import html2markdown
# import html5lib

# h = html5lib.HTMLParser(tree=html5lib.getTreeBuilder("dom"))
# s = h.parse('<div><h1>hello world</h1><table><tr><td>xxxxx</td></tr></table></div>').toxml()
# print(s)

h2m = html2markdown()
print( h2m.feed('<div><h1>hello world</h1><table><tr><td>xxxxx</td></tr></table></div>') )
# print( h2m.convert('<div><h1>hello world</h1><table><tr><td>xxxxx</td></tr></table></div>') )