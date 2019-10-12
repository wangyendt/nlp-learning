#!/usr/bin/env python
# encoding: utf-8

"""
@author: Wayne
@contact: wangye.hope@gmail.com
@software: PyCharm
@file: beautifulsoup
@time: 2019/10/10 11:34
"""
from bs4 import BeautifulSoup

html = """
<html><head><title2 a=b>Hello</title2></head></html>
"""
soup = BeautifulSoup(html, 'lxml')
print(soup.prettify())
print(soup.title2.string)
print(soup.title2.attrs)
print(soup.title2['a'])
print(soup.contents)
