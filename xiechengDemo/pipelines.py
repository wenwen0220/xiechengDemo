# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import os
import pymysql
from twisted.enterprise import adbapi
class JsonPipeline(object):
	def __init__(self):
		self.file = codecs.open('/Users/didi/jw/python/xiechengDemo/sceneryCode.json', 'w', encoding='utf-8')
		self.file.write('[')

	def process_item(self, item, spider):
		if spider.name == 'sceneryCode':
			# print("--------------",item)
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			self.file.write(line+',')
		return item

	def close_spider(self, spider):
		self.file.seek(-1, os.SEEK_END)
		self.file.truncate();
		self.file.write(']')
		self.file.close()

class MySQLPipeline(object):
	def __init__(self,dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls,settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
		"""
		数据库建立连接
		:param settings: 配置参数
		:return: 实例化参数
		"""
		adbparams = dict(
		host=settings['MYSQL_HOST'],
		db=settings['MYSQL_DB_NAME'],
		user=settings['MYSQL_USER'],
		password=settings['MYSQL_PASSWORD'],
		cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
		)
		# 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
		dbpool = adbapi.ConnectionPool('pymysql',**adbparams)
		# 返回实例化参数
		return cls(dbpool)
	def process_item(self, item, spider):
		if spider.name == 'sceneryComment':
			"""
			使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
			"""
			query = self.dbpool.runInteraction(self.insert_comment,item)  # 指定操作方法和操作数据
			# 添加异常处理
			query.addCallback(self.handle_error)  # 处理异常

		#这里必须return才能被下一个pipline处理，否则下一个pipline编程none
		return item
		 
	def insert_comment(self,cursor,item):
		# 对数据库进行插入操作，并不需要commit，twisted会自动commit
		insert_sql = 'insert into xiecheng_scenery_comment(id,uid,title,content,date,score,sceneryCode,sceneryName) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(insert_sql,(
			item['id'],
			item['uid'],
			item['title'],
			item['content'],
			item['date'],
			item['score'],
			item['sceneryCode'],
			item['sceneryName']))
	
	def handle_error(self,failure):
		if failure:
			# 打印错误信息
			print(failure)

