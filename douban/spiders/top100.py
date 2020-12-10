import scrapy


class Top100Spider(scrapy.Spider):
    name = 'top100'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com/doulist/13704241/']

    def parse(self, response):
        pass
