# 抓取博客园或其他博客的文章
#
# Author: Wang Shiqiang
#
# 思路一：从列表页面获取文章链接，然后依次抓取文章
# 思路二：从第一篇文章开始，依次获取上一篇文章直到最后
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
            get_cnblogs(arg)
        else:
            print("Usage: python3 main.py -l <blog_post_list_link>")

# 抓取cnblogs
def get_cnblogs(url):
    # 判断是否是首页
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    # 获取最新一篇文章链接
    lastest_blog_link = get_latest_link(soup)

    # 递归获取链接内容，获取图片
    # 
    # 保存到指定目录和文件名格式
    # 目录格式： cnblogs/htmls
    #                 /markdowns
    # 文件名格式: yyyy-mm-dd-blog-name.html
    
    # 转换为Markdown 文档

    pass

# 从博客园首页获取第一篇文章内容
def get_latest_link(bs4_soup):
    posts = bs4_soup.findAll('div', attrs={'class':'day'})
    return posts[0].find('a', attrs={'class':'postTitle2'})['href']


# 解析列表
def parse_list(url):
    all_posts = []
    html = get_html(url)
    next_page_link = ''

    # 解析单个列表页，获取所有文章链接信息
    single_page_posts, next_page_link = bs4_parse_link_lists(html)
    all_posts.append(single_page_posts)

    while next_page_link:
        print(next_page_link)
        html = get_html(next_page_link)
        single_page_posts, next_page_link = bs4_parse_link_lists(html)
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

    next_page = parse_next_page_link(soup)

    return all_posts, next_page

# 判断传入的是首页还是列表页，获取下一页链接地址
def parse_next_page_link(bs4_soup):
    next_page = bs4_soup.find('div', attrs={'id':'nav_next_page'})
    if next_page is not None and len(next_page) > 0:
        next_page = next_page.a['href']
    elif bs4_soup.find('div', attrs={'id':'homepage_top_pager'}):
        print("XXXXX")
        pager = bs4_soup.find('div', attrs={'id':'homepage_top_pager'})
        link_lists = pager.find_all('a')
        print(link_lists)
        next_page = False
    # print(next_page.a['href'])
    
    return next_page

if __name__ == "__main__":
    # print(__name__)
    main(sys.argv[1:])