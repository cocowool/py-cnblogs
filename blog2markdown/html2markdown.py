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

from html.parser import HTMLParser
try:
    from bs4 import BeautifulSoup
except:
    print("BeautifulSoup doesn't exist! Please run pip3 install beautifulsoup")

class html2markdown():
    # 定义DOM标签到Markdown标签的转换规则
    __rule_replacement = {
        'div'   : ('', ''),
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
        'tr'    : ('',''),
        'td'    : ('', ' |'),
        'br'    : ('', '\n')
        # a
        # img
        # table
        
    }

    # 分别处理每种支持的标签
    def _traverseDom(self, tag):
        md_string = ''

        if tag.children:
            for child in tag.children:
                # print(child.name)
                # print(type(child))
                if child.name != None:
                    # 处理TR
                    if child.name == "tr":
                        md_string += "| "
                        md_string += self._traverseDom(child)
                    elif child.name == "th":
                        md_string += "| "
                        md_string += self._traverseDom(child)
                        n = len(child.contents)
                        while n > 0:
                            md_string += "| ------------- "
                            n = n - 1
                        md_string += "|"
                    else:
                        md_string += self._traverseDom(child)
                else:
                    print(tag.name)
                    # print(tag.string)
                    # print(self._convertToMardown(tag.name, tag.string))
                    md_string += self._convertToMardown(tag.name, tag.string)
        else:
            print(tag.name)
            return tag.name

        return md_string        
        #     children = tag.find_all(recursive=False)
        #     for child in children:
        #         child = self._traverseDom(child)
        #     return

        # if tag.name in self.__rule_replacement:
        #     print(tag.name)
        #     print(self.__rule_replacement[tag.name])
        #     print(tag)
        #     tag.unwrap()
        #     print("===== After unwrap ======")
        #     print(tag)

        # # children = tag.find_all(recursive=False)
        # # for child in children:
        # #     tag = self._traverseDom(child)

        # return tag

    def _convertToMardown(self, tagName, string):
        if tagName in self.__rule_replacement:
            return self.__rule_replacement[tagName][0] + string + self.__rule_replacement[tagName][1]
        else:
            return False

    def convert(self, html_string, template = ''):
        soup = BeautifulSoup(html_string, 'html.parser')

        print(html_string)
        print('----- Begin Convert ----')
        soup = self._traverseDom(soup)

        print("========= Convert Result ==========")
        print(soup)

        print("----- Test -----")
        print(self.__rule_replacement['h1'][0])
        # print('div' in self.__rule_replacement)

        # # print(soup.find_all(recursive=True))
        # # print("XXXXXXX")

        # # if not soup.contents :
        # #     return soup.get_text()

        return True
        # for child in soup.descendants:
        #     print(child)

    def convertFile(self, income_file_path, outcome_file_path):
        pass