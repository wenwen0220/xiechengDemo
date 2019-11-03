# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field


class SceneryCodeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #最后的结果对象
    # _id=Field()
    provinceName=Field()
    cityName=Field()
    sceneryName=Field()
    sceneryCode=Field()

class SceneryCommentsItem(scrapy.Item):
	id=Field()
	uid=Field()
	title=Field()
	content=Field()
	date=Field()
	score=Field()
	sceneryCode=Field()
	sceneryName=Field()
		
