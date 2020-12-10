import re

import scrapy
from lxml import etree

from douban.items import Top100Item


def replace_newlines_and_spaces(origin: str) -> str:
    return origin.replace('\n', '').replace(' ', '')

def get_item_by_name(name: str, origin: str) -> str:
    pattern = f'{name}:(.*?)\n'
    result = re.findall(pattern, origin, re.S)
    return result[0] if result else ''


class Top100Spider(scrapy.Spider):
    name = 'top100'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com/doulist/13704241/']

    def parse(self, response):
        html = etree.HTML(response.text)
        subjects = html.xpath('//div[@class="doulist-item"]')

        for subject in subjects:
            if not subject.xpath('.//div[@class="bd doulist-subject"]'):
                continue
            no = subject.xpath('.//span[@class="pos"]/text()')[0]
            title = replace_newlines_and_spaces(''.join(subject.xpath('.//div[@class="title"]/a/text()')))
            abstract = ''.join(subject.xpath('.//div[@class="abstract"]/text()'))
            director = get_item_by_name('导演', abstract)
            starrings = get_item_by_name('主演', abstract)
            movie_type = get_item_by_name('类型', abstract)
            region = get_item_by_name('制片国家/地区', abstract)
            years = get_item_by_name('年份', abstract)
            cover_image = subject.xpath('.//div[@class="post"]/a/img/@src')[0]
            item = Top100Item(
                no=no,
                title=title,
                director=director,
                starrings=starrings,
                movie_type=movie_type,
                region=region,
                years=years,
                cover_image=cover_image
            )
            yield item
        
        next_url = html.xpath('//span[@class="next"]/a/@href')
        if next_url:
            yield scrapy.Request(next_url[0], callback=self.parse)

            
