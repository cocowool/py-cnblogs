import scrapy

# 抓取博客文章详细信息
class DetailSpider(scrapy.Spider):
    name = "detail"

    def start_requests(self):
        urls = [
            'https://www.cnblogs.com/cocowool/default.html?page=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        detail_list = response.css('div.postTitle > a::attr(href)').extract()
        for detail_page in detail_list:
            yield scrapy.Request(url=detail_page, callback=self.parse_detail)

        # 判断首页，倒数第二页和中间页的情况
        next_page = response.css('div#nav_next_page > a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            self.log('Next page is %s' %next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            pager = response.css('div.pager').re('末页')
            if pager is not None:
                next_page = response.css('div.pager > a::attr(href)').extract()[-2]
            elif response.css('div.pager').re('下一页') is not None:
                next_page = response.css('div.pager > a::attr(href)').extract()[-1]

            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        

    def parse_detail(self, response):
        page = response.url.split("/")[-1]
        filename = 'blog_html_files/blog_detail-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

        self.log('Save file %s' % filename)

