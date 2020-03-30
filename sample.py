from blog2markdown import html2markdown

h2m = html2markdown()

print( h2m.convert('<div><h1>hello world</h1><table><tr><td>xxxxx</td></tr></table></div>') )