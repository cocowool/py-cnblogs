import os, sys, re, glob, getopt
import html2text
from bs4 import BeautifulSoup
# 将CNBLOGS上的HTML格式的博客文章转换为Markdown格式
# Author: Wang shiqiang
# Email: cocowool@qq.com

# 入口函数，支持输入文件名和输入目录两种方式进行文件转换
def main(argv):
    try :
        opts,args = getopt.getopt(argv,"hf:d:",["file=","diretory="])
    except getopt.GetoptError:
        print("Usage: python html2md_cnblog.py -file <filename> -folder <folder_path>")

    for opt, arg in opts:
        if opt in ("-f", "--file"):
            html2md(arg)
            pass
        elif opt in ("-d", "--directory"):
            html2md(arg, "", "d")
            pass
        else:
            print("Usage: python html2md_cnblog.py -file <filename> -folder <folder_path>")

# 将HTML文件转换为MD文件
def html2md(income_file, outcome_file = "", income_type="f"):
    if income_type == "f":
        singleHtml2md(income_file, "test.md", "f")
    elif income_type == "d":
        for sourcefile in glob.glob(os.path.join(income_file,"*.html")):
            # print(sourcefile)
            singleHtml2md(sourcefile, "", "d")

# 将单个文件转换为Markdown格式的文档
def singleHtml2md(income_file, outcome_file = "", income_type="f"):
    # Hexo 需要的三个元素，title，date，tag
    hexo_title = ""
    hexo_date = ""
    # hexo_tag = ""

    # 打开文档
    file = open(income_file, 'r')
    # print(file.name)
    new_filename = file.name.split('/')[-1].split(".")[0]
    article = file.read()
    # print(article)
    # 处理CNBLOGS的原始文件，将不必要的头部内容和侧边栏去掉
    hexo_title = re.search(r'<title>(.*)</title>', article).group(1).split("-")[0]
    hexo_date = re.search(r'<span id="post-date">(.*)</span>\s', article).group(1)

    hexo_top = '''---
title: {hexo_title}
date: {hexo_date}
tag: 
---\n'''.format(hexo_title=hexo_title, hexo_date=hexo_date)

    # print(hexo_top)

    h2md = html2text.HTML2Text()
    h2md.ignore_links = False
    article = h2md.handle(article)

    if outcome_file == "":
        outcome_file = "./output/" + new_filename + ".md"

    with open(outcome_file, "w", encoding='utf8') as f:
        lines = article.splitlines()
        counter = 1
        skip_line = False
        for line in lines:
            if line[0:6] == "posted":
                hexo_date = line[9:25]
                skip_line = True
            if counter == 1:
                f.write(hexo_top)

            # 前15行都是无用的信息
            if counter >= 17 and skip_line == False:
                if line.endswith('-'):
                    f.write(line)
                else:
                    f.write(line+"\n")

            counter += 1

if __name__ == "__main__":
    # print(__name__)
    main(sys.argv[1:])