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

import traceback
import os, sys
import re
from html.parser import HTMLParser
try:
    from bs4 import BeautifulSoup
    from bs4 import NavigableString, Comment
except:
    print("BeautifulSoup doesn't exist! Please run pip3 install beautifulsoup")

# sys.setrecursionlimit(1000000)

class html2markdown():
    # 定义DOM标签到Markdown标签的转换规则
    __rule_replacement = {
        '[document]'    : ('',''),
        'div'   : ('', '\n'),
        'p'     : ('','\n'),
        'h1'    : ('\n# ', '\n'),
        'h2'    : ('\n## ', '\n'),
        'h3'    : ('\n### ', '\n'),
        'h4'    : ('\n#### ', '\n'),
        'h5'    : ('\n##### ', '\n'),
        'h6'    : ('\n###### ', '\n'),
        'code'  : ('```', '```\n'),
        'em'  : ('**', '**'),
        'strong'  : ('**', '**'),
        'blockquote'  : ('> ', '\n'),
        'table' : ('\n', ''),
        'tr'    : ('',''),
        'td'    : ('', ' | '),
        'br'    : ('', '\n'),
        'pre'   : ('', ''),
        'ul'    : ('\n','\n'),
        'li'    : ('* ', '\n'),
        'a'     : "[{}]({})",
        'span'  : ('', ''),
        'img'   : "![{}]({})"
    }

    # 分别处理每种支持的标签
    def _traverseDom(self, tag, md_string = ''):
        try:
            # print(tag.name)
            if isinstance(tag, Comment):
                pass
            elif isinstance(tag, NavigableString):
                md_string = self._convertText(tag, md_string)
            elif tag.name == '[document]':
                for child in tag.children:
                    md_string = self._traverseDom(child, md_string)
            elif tag.name == 'a':
                md_string = self._convertLink(tag, md_string)
            elif tag.name == 'img':
                md_string = self._convertImg(tag, md_string)
            elif tag.name == "table":
                md_string += '\n' + self._convertTable(tag, '')
            # elif len(tag.contents) <= 1:
            #     md_string = self._convertElement(tag, md_string)
            else:
                # print(tag.contents)
                for child in tag.children:
                    md_string += self._traverseDom(child, '')

                tag.clear()
                md_string = self._convertElement(tag, md_string)
                # print(tag.name)
                # print(md_string)
        except:
            traceback.print_exc()

        return md_string   

    # Convert general element
    def _convertText(self, tag, md_string):
        text = re.compile(r'[\s]+').sub(' ', tag.string)
        # text = text.lstrip().rstrip()
        md_string += text

        return md_string

    # Convert Img element
    def _convertImg(self, tag, md_string):
        md_string += self.__rule_replacement['img'].format(tag.get('alt') or '', tag.get('src') or '')

        return md_string

    # 转换链接 a 元素
    # Convert Element A
    def _convertLink(self, tag, md_string):
        inner_string = ''
        for child in tag.children:
            inner_string = self._traverseDom(child, inner_string)
        
        if inner_string != '':
            md_string += self.__rule_replacement['a'].format(inner_string, tag.get('href') or tag.get_text(strip=True))

        return md_string

    # 转换table元素，是否要考虑table的td中有样式的情况？
    # Convert table element
    def _convertTable(self, tag, md_string):
        for child in tag.children:
            if child.name == 'tr':
                md_string += "| "
                md_string += self._convertTable(child, '')
                md_string += "\n"
            elif child.name == 'th':
                md_string += "| "
                md_string += self._convertTable(child, '')
                md_string += "\n"
                # Add markdown thead row
                n = len(tag.contents)
                # print(tag.contents)
                while n > 0:
                    md_string += "| ------------- "
                    n = n - 1
                md_string += "| \n"
            elif child.name == 'td':
                md_string += self.__rule_replacement[child.name][0] + child.string + self.__rule_replacement[child.name][1]
            
        return md_string

    # 将HTML标签元素按照预定义规则进行转换
    def _convertElement(self, tag, md_string):
        inner_string = ''
        if tag.string is not None:
            inner_string = tag.string.lstrip().rstrip()

        if tag.name in self.__rule_replacement:
            # print(tag.name)
            # print(md_string)
            return self.__rule_replacement[tag.name][0] + md_string + inner_string + self.__rule_replacement[tag.name][1]
        else:
            raise Exception("Unsupported Tag " + tag.name + " !")

    # Convert html string entrance
    def convert(self, html_string, template = ''):
        soup = BeautifulSoup(html_string, 'html.parser')

        # id="post_detail" / cnblogs 模版
        # 
        container = soup.select_one('#post_detail') \
            or soup.select_one('body') \
            or soup

        # print(container.prettify())
        # print('----- Begin Convert ----')
        return self._traverseDom(container)

    # Convert File entrance 
    def convertFile(self, income_file_path, outcome_folder = ''):
        with open(income_file_path) as html_file:
            html_string = html_file.read()

        md_string = self.convert(html_string)

        if outcome_folder != '':
            with open(outcome_folder + "/" + income_file_path.split('/')[-1].split('.')[0] + ".md", 'w') as f:
                # print(md_string)
                f.write(md_string)
                f.close()
        else:
            return md_string

    # Conver htmls under a folder
    def convertFolder(self, income_folder, outcome_folder = ''):
        if not os.path.exists(income_folder):
            print("Income folder : " + income_folder + " does not exists!")
            return False

        for root, dirs, files in os.walk(income_folder):
            for f in files:
                self.convertFile(os.path.join(root,f), outcome_folder)
        pass