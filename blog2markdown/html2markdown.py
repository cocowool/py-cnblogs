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
    # 定义DOM标签到Markdown标签的转换规则
    __rule_replacement = {
        'div'   : ('', '\n'),
        'p'     : ('','\n'),
        'h1'    : ('# ', '\n'),
        'h2'    : ('## ', '\n'),
        'h3'    : ('### ', '\n'),
        'h4'    : ('#### ', '\n'),
        'h5'    : ('##### ', '\n'),
        'h6'    : ('###### ', '\n'),
        'code'  : ('```', '```'),
        # a
        # img
        # table
        
    }

    def __init__(self):    
        print("Html to Markdown module")

    def convert(self, html_string):
        soup = BeautifulSoup(html_string, 'html.parser')

        if not soup.contents :
            return soup.get_text()

        for child in soup.descendants:
            print(child)

    def convertFile():
        pass