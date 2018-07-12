import scrapy

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogsSpider'
    start_url = ['http://www.cnblogs.com/cocowool/']

    def parse(self, response):
        for title in response.css('h1.postTitle'):
            yield {'title':title.css('a ::text').extract_first()} }

        for next_page in response.css('div.post_next_prev > a'):
            yield response.follow(next_page, self.parse)

