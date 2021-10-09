# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CityspiderItem(scrapy.Item):
    # define the fields for your item here like:
    city_name = scrapy.Field()
    link = scrapy.Field()
    img = scrapy.Field()
    brief = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    utc = scrapy.Field()
    nation = scrapy.Field()
    area = scrapy.Field()
    pop = scrapy.Field()
