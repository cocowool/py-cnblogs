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

import os, sys
from html.parser import HTMLParser
try:
    from bs4 import BeautifulSoup
    from bs4 import NavigableString, Doctype
except:
    print("BeautifulSoup doesn't exist! Please run pip3 install beautifulsoup")

class html2markdown():
    # 定义DOM标签到Markdown标签的转换规则
    __rule_replacement = {
        '[document]'    : ('',''),
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
        'table' : ('\n', ''),
        'tr'    : ('',''),
        'td'    : ('', ' | '),
        'br'    : ('', '\n'),
        'pre'   : ('', ''),
        'li'    : ('* ', '\n'),
        # a
        # img
        # table
        
    }

    # 分别处理每种支持的标签
    def _traverseDom(self, tag):
        try:
            print(type(tag))
            # print("Tag.name = " + tag.name)
            if isinstance(tag, NavigableString):
                print("Here navigableString")
                print("NavigableString: " + tag.name)
            elif isinstance(tag, Doctype):
                print("Here doctype")
                print("Doctype: " + tag.name)
            else:
                for child in tag.children:
                    self._traverseDom(child)
        except:
            print("Error")

        return True

        md_string = ''
        print(tag.name)
        try:
            for child in tag.children:
                print(type(child))
                if isinstance(child, NavigableString):
                    return True
                else:
                    self._traverseDom(child)
                # if( child.children):
                # print(child.name)
                # print(len(child.children))
                # print(len(child.contents))
        except:
            print(child.contents)
        # else:
        #     print("No Children")

        return True

        if tag.children:
            for child in tag.children:
                print(child.name)
                # print(type(child))
                if child.name != None:
                    # 处理TR
                    if child.name == "tr":
                        md_string += "| "
                        md_string += self._traverseDom(child)
                        md_string += "\n"
                    elif child.name == "th":
                        md_string += "| "
                        md_string += self._traverseDom(child)
                        md_string += "\n"
                        # Add markdown thead row
                        n = len(child.contents)
                        while n > 0:
                            md_string += "| ------------- "
                            n = n - 1
                        md_string += "| \n"
                    else:
                        md_string += self._traverseDom(child)
                else:
                    # print(tag.name)
                    # print(tag.string)
                    # print(self._convertToMardown(tag.name, tag.string))
                    md_string += self._convertToMardown(tag.name, tag.string)
        else:
            # print(tag.name)
            return tag.name

        return md_string        

    def _convertToMardown(self, tagName, string):
        if tagName in self.__rule_replacement:
            # print(tagName)
            return self.__rule_replacement[tagName][0] + string + self.__rule_replacement[tagName][1]
        else:
            raise Exception("Unsupported Tag " + tagName + " !")

    def convert(self, html_string, template = ''):
        soup = BeautifulSoup(html_string, 'html5lib')

        # id="post_detail" / cnblogs 模版
        # 
        container = soup.select_one('#post_detail') \
            or soup.select_one('body') \
            or soup

        # print(html_string)
        print('----- Begin Convert ----')
        md_string = self._traverseDom(soup)

        print("========= Convert Result ==========")
        # print(soup)

        # print("----- Test -----")
        # print(self.__rule_replacement['h1'][0])
        # print('div' in self.__rule_replacement)

        # # print(soup.find_all(recursive=True))
        # # print("XXXXXXX")

        # # if not soup.contents :
        # #     return soup.get_text()

        return md_string
        # for child in soup.descendants:
        #     print(child)

    def convertFile(self, income_file_path, outcome_file_path = ''):
        with open(income_file_path) as html_file:
            html_string = html_file.read()
            self.convert(html_string)

        pass