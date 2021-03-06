# -*- coding:utf-8 -*-
import requests
from pyquery import PyQuery as pq
import re
import pandas as pd
import time
import random
import string

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]



dataframe = pd.DataFrame()

'''name = raw_input("请输入电影名字")

url = "https://movie.douban.com/subject_search?search_text="+ name +"&cat=1002"

r = requests.get(url)

print r.text
print url
'''
'''
for i in range(0,250,25):
	#待爬取的网址
	url = 'https://movie.douban.com/top250?start=%d&filter='%i
	#爬取url，获取内容
	r = requests.get(url)

	#遍历
	for movie in pq(r.text).find('.item'):
		print pq(movie).find('.title').html(),"  ",
		print pq(movie).find('.rating_num').html(),
		#print pq(movie).find('.bd').html()'''

class Douban_url:
	"""获取所有 """
	def __init__(self):
		self.url_list = []
		self.headers = {}
	def get_headers(self):
		self.headers = {
	        "User-Agent": random.choice(USER_AGENTS),
	        "Host": "movie.douban.com",
	        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	        "Accept-Encoding": "gzip, deflate, sdch, br",
	        "Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
	        "Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
    	}

	def get_url(self,page,url):
		#print pq(page).find('.next').attr('href')
		return url + pq(page).find('.next').find('a').attr('href')
	def downloader(self,url):
		r = requests.get(url,headers=self.headers)
		return r.text
	def html_paser(self,page):
		for item in pq(page).find('.item'):
			url = pq(item).find('.pic').find('a').attr('href') + 'comments?status=P'
			#print url
			self.url_list.append(url)
	def start(self):
		url_start = 'https://movie.douban.com/top250'
		url_root = url_start.split('?')[0]
		#print url_root
		url = url_start
		while(True):
			#print url
			try:
				self.get_headers()
				page = self.downloader(url)
				self.html_paser(page)
				url = self.get_url(page,url_root)
			except Exception as e:
				#print e
				break
	def get_list(self):
		return self.url_list

class Douban:
	"""demo """
	def __init__(self,url_start):
		self.url_start = url_start
		self.data = []
		self.headers = {}
	def get_headers(self):
		self.headers = {
	        "User-Agent": random.choice(USER_AGENTS),
	        "Host": "movie.douban.com",
	        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	        "Accept-Encoding": "gzip, deflate, sdch, br",
	        "Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
	        "Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
    	}
	def get_url(self,page,url):
		#print pq(page).find('.next').attr('href')
		return url + pq(page).find('.next').attr('href')
	def downloader(self,url):
		r = requests.get(url,headers=self.headers)
		return r.text
	def html_paser(self,page,movie):
		for item in pq(page).find('.comment-item'):
			user = pq(item).find('.comment-info').find('a').html()
			rating = pq(item).find('.rating').attr('title')
			time = pq(item).find('.comment-time').attr('title')
			text = pq(item).find('.comment').find('p').html()
			self.data.append({'movie':movie,'user':user,'rating':rating,'time':time,'text':text})
	def output(self):
		for item in self.data:
			#dataframe = pd.DataFrame({'title':item['title'],'rating':item['rating']})
			print item['title'],"  ",item['rating']
		#dataframe.to_csv("test.csv",sep=',')
	def writefile(self):
		global num
		df = pd.DataFrame(self.data,columns=['movie','user','rating','time','text'])
		df.to_csv('w.csv', sep=',', header=False, index=False,encoding='utf-8',mode='a')
	def start(self,num=250):
		url_root = self.url_start.split('?')[0]
		#print url_root
		url = self.url_start
		while(True):
			time.sleep(2)
			print url
			try:
				self.get_headers()
				page = self.downloader(url)
				movie = pq(page).find('#content').find('h1').html()
				movie = movie.split(' ')[0]
				#print movie
				self.html_paser(page,movie)
				url = self.get_url(page,url_root)
			except Exception as e:
				#print e
				break
			
		self.writefile()
	
'''	
		for url in self.get_url(num):
			page = self.downloader(url)
			self.html_paser(page)
		self.output()
		self.writefile()'''

#d = Douban()
#d.start()
u = Douban_url()

u.start()
url_list = u.get_list()
df = pd.DataFrame(columns=['movie','user','rating','time','text'])
df.to_csv('w.csv', sep=',', header=True, index=False,encoding='utf-8',mode='a')
while(len(url_list)>0):
	d = Douban(url_list.pop())
	d.start()
	time.sleep(120)

#print cookies

