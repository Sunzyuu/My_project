# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WordsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    word = scrapy.Field()
    soundmark = scrapy.Field()
    url = scrapy.Field()
    translation = scrapy.Field()

