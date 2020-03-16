# 抓取博客园或其他博客的文章
#
# Author: Wang Shiqiang
import os, sys, getopt
import re
import requests
from bs4 import BeautifulSoup

# 入口函数，输入文章列表页地址后进行文件抓取
def main(argv):
    try :
        opts,args = getopt.getopt(argv,"hl:",["link="])
    except getopt.GetoptError:
        print("Usage: python3 main.py -l <blog_post_list_link>")

    for opt, arg in opts:
        if opt in ("-l", "--link"):
            parse_list(arg)
        else:
            print("Usage: python3 main.py -l <blog_post_list_link>")


def parse_list(url):
    html = get_html(url)

    soup = bs4_parse(html)

# 通过requests方式获取网页内容
def get_html(url, method = "requests"):
    response = requests.get(url)

    return response.text

# 使用BeautifulSoup解析HTML
def bs4_parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    post_lists = soup.find_all('div', attrs={'class':'day'})
    print(post_lists)

if __name__ == "__main__":
    # print(__name__)
    main(sys.argv[1:])