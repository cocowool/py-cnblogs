# 抓取博客园或其他博客的文章, 保存为HTML文件
#
# Author: Wang Shiqiang
#
# 思路一：从列表页面获取文章链接，然后依次抓取文章。
# 思路二：从第一篇文章开始，依次获取上一篇文章直到最后。发现CNBLOGS的上一篇、下一篇是通过Ajax加载的，给抓取造成了一些困难。
import os, sys, getopt
import re
import requests
import json
from bs4 import BeautifulSoup

class blog2html():
    html_path = ''
    markdown_path = ''

    # 读取配置文件
    # TODO检查配置文件是否存在
    def read_config(self):
        with open("config.json") as json_file:
            config = json.load(json_file)

        return config

    # 抓取cnblogs
    def get_cnblogs(self, url):
        # 测试Ajax地址获取
        # html = get_html("https://www.cnblogs.com/cocowool/ajax/post/prevnext?postId=12507681")
        # print(html)
        # return True

        # 判断是否是首页
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        # 创建指定的目录
        # 目录格式： cnblogs-{blog-title}/htmls
        #                              /markdowns
        self.mkdir_cnblogs(url)

        # 获取最新一篇文章链接
        lastest_blog_link = self.get_latest_link(soup)

        # 递归获取链接内容，获取图片
        # 保存到指定目录和文件名格式
        # 文件名格式: yyyy-mm-dd-blog-name.html
        self.get_all_posts(lastest_blog_link, url)
            
    # 遍历抓取cnblogs博客
    def get_all_posts(self, blog_link, home_link):
        print("GET " + blog_link)
        html = self.get_html(blog_link)
        soup = BeautifulSoup(html, 'html.parser')

        # 规范文件名: yyyy-mm-dd-blog-name.html
        post_date = soup.find('span', attrs={'id':'post-date'}).contents[0].split(" ")[0]
        blog_file_name = post_date + "-" + blog_link.split("/")[-1]

        # 解析文件中的图像并保存，并将图片地址替换为相对地址
        html_content = self.save_images(soup, blog_file_name)

        self.save_html_file(blog_file_name, str(html_content) )
        print("DONE :" + blog_link)

        # 通过Ajax获取上一篇链接
        blog_entry_id = re.search(r'cb_entryId\s=\s(\d+)',html).group().split("=")[1].strip()
        ajax_link = home_link + "ajax/post/prevnext?postId=" + blog_entry_id
        page_html = self.get_html(ajax_link)
        page_soup = BeautifulSoup(page_html, 'html.parser')

        if page_soup.a['href'] and len( page_soup.text.split("上一篇")) > 1:
            self.get_all_posts(page_soup.a['href'], home_link)
        else:
            print("The last blog finished !")


    # 保存HTML文件
    def save_html_file(self, filename, file_content):
        f = open(self.html_path + filename, 'wb')
        f.write(str.encode(file_content))
        f.close()

    # 创建预定的目录结构
    def mkdir_cnblogs(self, url):
        blog_title = url.split('.com/')[1].split('/')[0]

        self.html_path = "./cnblogs{}/htmls/".format('-'+blog_title)
        self.markdown_path  = "./cnblogs{}/markdowns/".format('-'+blog_title)

        isExists_html = os.path.exists(self.html_path)
        isExists_markdown = os.path.exists(self.markdown_path)
        
        if (not isExists_html) and (not isExists_markdown):
            os.makedirs(self.html_path)
            os.makedirs(self.markdown_path)

            return True
        else:
            return False

    # 从博客园首页获取第一篇文章内容
    def get_latest_link(self, bs4_soup):
        posts = bs4_soup.findAll('div', attrs={'class':'day'})
        return posts[0].find('a', attrs={'class':'postTitle2'})['href']


    # 解析列表
    def parse_list(self, url):
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
    def get_html(self, url, method = "requests"):
        config = self.read_config()

        my_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'
        }

        if config['cookie']:
            my_cookie = config['cookie']

        response = requests.get(url, headers = my_headers, cookies = my_cookie)

        return response.text

    # 创建一个同名文件夹，用于存放图片
    def save_images(self, bs4_html, blog_file_name):
        html_path = self.html_path + blog_file_name.split('.')[0]
        markdown_path  = self.markdown_path + blog_file_name.split('.')[0]

        # 检查图片保存路径
        if (not os.path.exists(html_path) ) and (not os.path.exists(markdown_path)):
            os.makedirs(html_path)
            os.makedirs(markdown_path)

        config = self.read_config()

        my_cookie = ''
        if config['cookie']:
            my_cookie = config['cookie']

        my_headers = ''
        if config['ua']:
            my_headers = config['ua']

        img_links = bs4_html.find_all('img')
        for img in img_links:
            # print(img.get('src').split('/')[-1])
            if re.search(r'http', img.get('src')):
                try:
                    req = requests.get(img.get('src'), headers = my_headers, cookies = my_cookie)
                    with open(markdown_path + "/" + img.get('src').split('/')[-1], 'wb') as f:
                        f.write(req.content)
                        f.close()

                    with open(html_path + "/" + img.get('src').split('/')[-1], 'wb') as f:
                        f.write(req.content)
                        f.close()

                    # 替换图片
                    new_img = bs4_html.new_tag("img")
                    new_img['src'] = "" + blog_file_name.split('.')[0] + "/" + img.get('src').split('/')[-1]
                    img.replace_with(new_img)
                except:
                    print("Get Image Error: " + img.get('src'))

        return bs4_html

    # 使用BeautifulSoup解析HTML，获取当前页面的链接信息
    def bs4_parse_link_lists(self, html):
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
    def parse_next_page_link(self, bs4_soup):
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

    # if __name__ == "__main__":
    #     # print(__name__)
    #     main(sys.argv[1:])