# 支持将html内容转换为markdown格式文档
# Author: Wang Shiqiang
# Date: 2020/03/30

# 支持将HTML元素转换为Markdown格式
# 
# 思路：
# (一)列出需要转换的元素，从HTML中搜索并替换相关元素
# (二)遍历DOM树，依次将遇到的元素做替换
# 
# 特性：
# * 支持博客园/CSDN等常见博客的模版

try:
    from bs4 import BeautifulSoup
except:
    print("BeautifulSoup doesn't exist! Please run pip3 install beautifulsoup")

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
        'em'  : ('**', '**'),
        'strong'  : ('**', '**'),
        'blockquote'  : ('> ', '\n'),
        # a
        # img
        # table
        
    }

    def __init__(self):    
        print("Html to Markdown module")

    # 分别处理每种支持的标签
    def _traverseDom(self, tag):

        if tag.name == 'document':
            children = tag.find_all(recursive=False)
            for child in children:
                child = self._traverseDom(child)
            return

        if tag.name == "div":
            # print('----------')
            # print(tag.name)
            # print('----------')
            # print(tag)
            tag.unwrap()

        children = tag.find_all(recursive=False)
        for child in children:
            child = self._traverseDom(child)

        return tag

    def convert(self, html_string, template = ''):
        soup = BeautifulSoup(html_string, 'html.parser')

        soup = self._traverseDom(soup)

        print(soup)

        # print(soup.find_all(recursive=True))
        # print("XXXXXXX")

        if not soup.contents :
            return soup.get_text()

        # for child in soup.descendants:
        #     print(child)

    def convertFile(self, income_file_path, outcome_file_path):
        pass