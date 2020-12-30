# 支持生成博客园的年度报告
# Author: Wang Shiqiang
# Date: 2020/12/30

# 报告的指标
# * 文章总数量
# * 文章阅读总量
# * 最高阅读量
# * 推荐总量
# * 最高推荐的文章
# * 评论的数量
# * 最多评论的文章
# * 最早发文的时间与文章名称
# * 最晚发文的时间与文章名称

import os, sys, getopt
import re
import requests
import json
from bs4 import BeautifulSoup

class generate():
    def __init__(self, blog_url, year = 2020):
        self.blog_url = blog_url
        self.year = year

    # 从列表页获取所有文章相关信息
    def _get_post_lists(self):
        blog_data = []

        html = requests.get(self.blog_url).text
        soup = BeautifulSoup(html, 'html.parser')

        # 获取下一页链接地址
        next_page = soup.find('div', attrs={'id':'nav_next_page'})
        next_page_link = next_page.a['href']
        
        # 保存本页的文章信息
        blog_data += soup.find_all('div', attrs={'class':'day'})

        while True:
            next_html = requests.get(next_page_link).text
            next_soup = BeautifulSoup(next_html, 'html.parser')
            blog_data += next_soup.find_all('div', attrs={'class':'day'})

            next_pager = next_soup.find('div', attrs={'id':'homepage_bottom_pager'})
            if "下一页" in next_pager.text:
                next_page_link = next_pager.find_all('a')[-1]['href']
            else:
                break


        return blog_data

    def run(self):
        print("Hello World")

        blog_data = self._get_post_lists()
        print(blog_data)
        print(len(blog_data))

        pass