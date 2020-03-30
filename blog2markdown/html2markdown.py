# 支持将html内容转换为markdown格式文档
# Author: Wang Shiqiang
# Date: 2020/03/30

# 支持将HTML元素转换为Markdown格式
# 
# 思路：
# (一)列出需要转换的元素，从HTML中搜索并替换相关元素
# (二)遍历DOM树，依次将遇到的元素做替换

from bs4 import BeautifulSoup

class html2markdown():
    def __init__(self):    
        print("Html to Markdown module")

    def convert(self, html_string):
        soup = BeautifulSoup(html_string, 'html.parser')

        if not soup.contents :
            return soup.get_text()

        
        print(soup.contents)
        pass

    def convertFile():
        pass