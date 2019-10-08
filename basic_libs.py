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

print(urllib.request.urlopen('http://www.baidu.com'))
print(requests.get('http://www.baidu.com'))
# driver = webdriver.Chrome()
# driver.get('http://www.baidu.com')
# pprint.pprint(driver.page_source)
# driver = webdriver.PhantomJS()
# driver.get('http://www.baidu.com')
# print(driver.page_source)

# soup = BeautifulSoup('<html></html>','lxml')
# print(soup)

doc = pq('<html>Hello</html>')
res = doc('html').text()
print(res)

client = pymongo.MongoClient('localhost')
db = client['newtestdb']
db['table'].insert({'name':'Bob'})
print(db['table'].find_one({'name':'Bob'}))

