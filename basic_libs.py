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

print(urllib.request.urlopen('http://www.baidu.com'))
print(requests.get('http://www.baidu.com'))
# driver = webdriver.Chrome()
# driver.get('http://www.baidu.com')
# pprint.pprint(driver.page_source)
driver = webdriver.PhantomJS()
driver.get('http://www.baidu.com')
print(driver.page_source)