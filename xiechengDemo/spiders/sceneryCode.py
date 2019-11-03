import scrapy
from xiechengDemo.items import SceneryCodeItem
import random
import re
#爬取景区的code
class SceneryCodeSpider(scrapy.Spider):
	name = "sceneryCode"
	#要爬取的url集合
	# start_urls = ['https://you.ctrip.com/sightlist/shandong100039/s0-p2.html']
	#可以直接读取文件
	start_urls=[i.strip() for i in open('/Users/didi/jw/python/xiechengDemo/urls.txt').readlines()]

	def parse(slf,response):
		# print(response)
		#用xpath获取需要的内容
		sceneryName_list=response.xpath('.//*[@class="list_mod2"]/div[2]/dl/dt/a/text()').extract()
		#获取景区的url连接地址
		sceneryUrl_list=response.xpath('.//*[@class="list_mod2"]/div[2]/dl/dt/a/@href').extract()
		# print(sceneryName_list)
		list=[]

		for i,j in zip(sceneryName_list,sceneryUrl_list):
			#将url切分，获取景区code与城市名称
			uri=j.split("/")
			sceneryItem=SceneryCodeItem()
			# item['_id']=str(random.randint(1,1000))
			sceneryItem['provinceName']= "shandong"
			#获取所有非数字的，正则表达式（qingdao）
			sceneryItem['cityName']= re.findall("\D+",uri[2])[0]
			sceneryItem['sceneryName']=i
			#获取所有数字的，正则表达式（1234）
			sceneryItem['sceneryCode']=re.findall("\d+",uri[3])[0]
			print(sceneryItem)
			yield sceneryItem
		# 	list.append(sceneryItem)
		# return list
