# 支持生成博客园的年度报告
# Author: Wang Shiqiang
# Date: 2020/12/30

import os, sys, getopt
import re
import requests
import json
from bs4 import BeautifulSoup

class generate():
    blog_title = ''

    def __init__(self, blog_url, year = 2020):
        self.blog_url = blog_url
        self.year = year

    # 从列表页获取所有文章相关信息
    def _get_post_lists(self):
        blog_data = []

        html = requests.get(self.blog_url).text
        soup = BeautifulSoup(html, 'html.parser')

        self.blog_title = soup.find('a', attrs={'id':'Header1_HeaderTitle'}).text.strip()

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

    # 将抓取的数据准备统计所需的格式
    def _prepare_data(self, blog_data):
        stat_data = []
        post_data = {}
        for item in blog_data:
            # print(item)
            post_data['post_title'] = item.find('div', attrs={'class':'postTitle'}).text.strip()
            # post_data['post_desc'] = item.find('div', attrs={'class':'c_b_p_desc'}).text.strip()
            post_data['post_date'] = re.search(r'\d{4}-\d{2}-\d{2}', item.find('div', attrs={'class':'postDesc'}).contents[0]).group()
            post_data['post_time'] = re.search(r'\d{2}:\d{2}', item.find('div', attrs={'class':'postDesc'}).contents[0]).group()
            post_data['view_count'] = int(re.search(r'\d+', item.find('span', attrs={'class':'post-view-count'}).text.strip()).group())
            post_data['digg_count'] = int(re.search(r'\d+', item.find('span', attrs={'class':'post-digg-count'}).text.strip()).group())
            post_data['comment_count'] = int(re.search(r'\d+', item.find('span', attrs={'class':'post-comment-count'}).text.strip()).group())

            stat_data.append(post_data)
            post_data = {}

        return stat_data

    # 计算统计指标
    # 报告的指标
    # * 文章总数量
    # * 文章阅读总量
    # * 最高阅读量
    # * 推荐总量
    # * 最高推荐的文章
    # * 评论的数量
    # * 最多评论的文章
    # * 最晚发文的时间与文章名称
    def _calc_stat(self, blog_data):
        stat_data = {}

        stat_data['total_post'] = len(blog_data)
        stat_data['year_post'] = 0
        stat_data['total_view'] = 0
        stat_data['total_comment'] = 0
        stat_data['total_digg'] = 0
        stat_data['max_view'] = {"view_count":0,"post_title":""}
        stat_data['max_comment'] = {"comment_count":0,"post_title":""}
        stat_data['max_digg'] = {"digg_count":0,"post_title":""}
        # stat_data['early_post'] = {}
        stat_data['late_post'] = {"post_time":"00:00", "post_title":""}

        for item in blog_data:
            stat_data['total_view'] += item['view_count']
            stat_data['total_comment'] += item['comment_count']
            stat_data['total_digg'] += item['digg_count']

            if item['view_count'] > stat_data['max_view']['view_count']:
                stat_data['max_view']['view_count'] = item['view_count']
                stat_data['max_view']['post_title'] = item['post_title']

            if item['comment_count'] > stat_data['max_comment']['comment_count']:
                stat_data['max_comment']['comment_count'] = item['comment_count']
                stat_data['max_comment']['post_title'] = item['post_title']

            if item['digg_count'] > stat_data['max_digg']['digg_count']:
                stat_data['max_digg']['digg_count'] = item['digg_count']
                stat_data['max_digg']['post_title'] = item['post_title']

            if item['post_date'] > '2019-12-31':
                stat_data['year_post'] += 1

            # 只考虑了0点以后发文的问题
            if item['post_time'] < '05:00' and item['post_time'] > stat_data['late_post']['post_time']:
                stat_data['late_post']['post_time'] = item['post_time']
                stat_data['late_post']['post_title'] = item['post_title']

        return stat_data

    def _render_md(self, stat_data):
        md_string = "## " + self.blog_title + " 的博客园年度报告\n"
        md_string += "Hi " + self.blog_title + '  '
        md_string += "你在博客园已经发表了**" + str(stat_data['total_post']) + "**篇文章\n" 
        md_string += "2020年你一共写了**" + str(stat_data['year_post']) + "**篇文章\n" 

        md_string += "\n"
        md_string += "你在博客园中的文章已经获得了**" + str(stat_data['total_view']) + "**次阅读\n" 
        md_string += "**" + str(stat_data['total_comment']) + "**评论以及**" + str(stat_data['total_digg']) + "**次推荐\n" 

        md_string += "\n"
        md_string += "你阅读量最高的一篇文章是 **" + stat_data['max_view']['post_title'] + "**，共有 **" + str(stat_data['max_view']['view_count']) + "** 次阅读\n"

        md_string += "\n"
        md_string += "**" + stat_data['late_post']['post_title'] + "** 是你在 **" + stat_data['late_post']['post_time'] + "** 写下的，夜已深注意休息\n"

        md_string += "\n"
        md_string += "新的一年，希望你继续笔耕不辍，在博客园发表更多的文章\n"

        return md_string

    def run(self):

        blog_data = self._get_post_lists()

        blog_data = self._prepare_data(blog_data)
        
        stat_data = self._calc_stat(blog_data)

        print(self._render_md(stat_data))

        pass