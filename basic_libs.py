#!/usr/bin/env python
# encoding: utf-8

"""
@author: Wayne
@contact: wangye.hope@gmail.com
@software: PyCharm
@file: basic_libs
@time: 2019/10/8 16:58
"""


import urllib
import urllib.request
import re
import requests
import selenium
from selenium import webdriver
import pprint
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import pymongo
import requests
from requests.packages import urllib3
urllib3.disable_warnings()

# print(urllib.request.urlopen('http://www.baidu.com'))
# print(requests.get('http://www.baidu.com'))
# driver = webdriver.Chrome()
# driver.get('http://www.baidu.com')
# pprint.pprint(driver.page_source)
# driver = webdriver.PhantomJS()
# driver.get('http://www.baidu.com')
# print(driver.page_source)

# soup = BeautifulSoup('<html></html>','lxml')
# print(soup)

# doc = pq('<html>Hello</html>')
# res = doc('html').text()
# print(res)
#
# client = pymongo.MongoClient('localhost')
# db = client['newtestdb']
# db['table'].insert({'name':'Bob'})
# print(db['table'].find_one({'name':'Bob'}))
#
# response = requests.get('http://www.baidu.com')
# print(response.text)
# print(response.headers)
# print(response.status_code)
#
#
# data = {
#     'name':'germey',
#     'age':22
# }
# response = requests.get('http://httpbin.org/get',params=data)
# print(response.text)
# response = requests.get('http://httpbin.org/get')
# print(response.json())
#
#
# response = requests.get('https://github.com/favicon.ico')
# with open('github.ico','wb') as f:
#     f.write(response.content)

# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
# }
# response = requests.get('https://www.zhihu.com/explore',headers=headers)
# print(response.status_code)


# s = requests.Session()
# s.get('http://httpbin.org/cookies/set/hello/world')
# response = s.get('http://httpbin.org/cookies')
# print(response.text)

# response = requests.get('https://www.12306.cn',verify=False)
# print(response.status_code)

# proxies = {
#     'http'
# }