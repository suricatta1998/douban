# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Top100Item(scrapy.Item):
    no = scrapy.Field()
    title = scrapy.Field()
    director = scrapy.Field()
    starrings = scrapy.Field()
    movie_type = scrapy.Field()
    region = scrapy.Field()
    years = scrapy.Field()
    cover_image = scrapy.Field()
    