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
    all_posts = []
    html = get_html(url)

    # 解析单个列表页，获取所有文章链接信息
    single_page_posts = bs4_parse_link_lists(html)
    all_posts.append(single_page_posts)

    print(all_posts)

# 通过requests方式获取网页内容
def get_html(url, method = "requests"):
    response = requests.get(url)

    return response.text

# 使用BeautifulSoup解析HTML，获取当前页面的链接信息
def bs4_parse_link_lists(html):
    # 用来存放所有博客标题、链接和创建日期
    all_posts = []
    single_post = {}
    soup = BeautifulSoup(html, 'html.parser')

    post_lists = soup.find_all('div', attrs={'class':'day'})
    for p in post_lists:
        post_link = p.find('a', attrs={'class':'postTitle2'})
        if post_link is not None and len(post_link) > 0:
            single_post['title'] = post_link.contents[0].strip()
            single_post['link'] = post_link['href']

        post_date = p.find('div', attrs={'class':'postDesc'})
        single_post['date'] = re.search(r'\d{4}-\d{2}-\d{2}', post_date.contents[0]).group()

        all_posts.append(single_post)
        single_post = {}

    return all_posts

if __name__ == "__main__":
    # print(__name__)
    main(sys.argv[1:])