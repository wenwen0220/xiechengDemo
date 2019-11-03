import scrapy
from xiechengDemo.items import SceneryCommentsItem
import random
import json
import re
import datetime
from datetime import date

#爬取景区的code
class SceneryCommentSpider(scrapy.Spider):
	name = "sceneryComment"

	def start_requests(self):

		postUrl="https://sec-m.ctrip.com/restapi/soa2/12530/json/viewCommentList"
		for data in self.getBody():
			#FormRequest方法的content-type默认是“application/x-www-form-urlencoded”，请求会返回空，用下边的方法替换。
			# yield scrapy.FormRequest(url=postUrl,formdata=data,callback=self.parse) 
			yield scrapy.Request(
				postUrl, 
				body=json.dumps(data[0]), 
				method='POST', 
				headers={'Content-Type': 'application/json'},
				callback=lambda response,sceneryCode=data[1],sceneryName=data[2]: self.parse(response,sceneryCode,sceneryName))

	def parse(slf,response,sceneryCode,sceneryName):
		# print(response.text)

		# date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		#获取今天的时间
		# today = date.today()
		beginDate=date(2019,1,1)


		jsonArray=json.loads(response.body)['data']['comments']
		for i in jsonArray:
			#评论日期
			# commentDate=datetime.datetime.strptime(i['date'],'%Y-%m-%d')
			#获取年-月-日，格式是str
			commentDateStr=datetime.datetime.strptime(i['date'], '%Y-%m-%d %H:%M').strftime('%Y-%m-%d')
			#str转换成datetime
			b=datetime.datetime.strptime(commentDateStr,'%Y-%m-%d')
			#datetime转换成date
			commentDate=datetime.datetime.date(b)
			# print("------is",commentDate)
			#不是2019年的就跳出
			if commentDate<beginDate :
				continue

			sceneryCommentsItem=SceneryCommentsItem()
			sceneryCommentsItem['id']=i['id']
			sceneryCommentsItem['uid']=i['uid']
			sceneryCommentsItem['title']=i['title']
			sceneryCommentsItem['content']=i['content']
			sceneryCommentsItem['date']=i['date']
			sceneryCommentsItem['score']=i['score']
			sceneryCommentsItem['sceneryCode']=sceneryCode
			sceneryCommentsItem['sceneryName']=sceneryName
			yield sceneryCommentsItem

	#获取body的方法
	def getBody(self):
		# f=open("/Users/didi/jw/python/xiechengDemo/sceneryCode.json")
		# res=f.read
		# jsonArray=json.load(res)
		#读取json文件
		listData=[]
		with open('/Users/didi/jw/python/xiechengDemo/sceneryCode.json','r') as f:
			#直接用load方法
			jsonArray=json.load(f)
		for i in jsonArray:
			# print(i['sceneryCode'])
			data={
				"pageid": "10650000804",
			    "viewid": i['sceneryCode'],
			    "tagid": "0",
			    "pagenum": "1",
			    "pagesize": "50",
			    "contentType": "json",
			    "head": {
			        "appid": "100013776",
			        "cid": "09031037211035410190",
			        "ctok": "",
			        "cver": "1.0",
			        "lang": "01",
			        "sid": "8888",
			        "syscode": "09",
			        "auth": "",
			        "extension": [
			            {
			                "name": "protocal",
			                "value": "https"
			            }
			        ]
			    },
			    "ver": "7.10.3.0319180000"
			}
			list=[]
			list.append(data)
			list.append(i['sceneryCode'])
			list.append(i['sceneryName'])
			listData.append(list)
		return listData

