#!/usr/bin/env python
# encoding: utf-8

"""
@author: Wayne
@contact: wangye.hope@gmail.com
@software: PyCharm
@file: weibo_comments.py
@time: 2019/11/18 16:54
"""

import pprint
from urllib.parse import urlencode

import requests
from fake_useragent import UserAgent

keywords = ['vivo nex3']
kw = keywords[0]
data = {
    'hideSearchFrame': '',
    'keyword': kw,
    'page': 100
}
ua = UserAgent(verify_ssl=False)
headers = {
    'user-agent': ua.random,
    'cookies': 'ALF=1576640241; SCF=Av3drcZ8yVY2VVOSyBGTQaWu2qSjzM6qrCgXTMir-D-mBGQDmoKY8D4_AKU8o1mKXpxIxSfgou1P68inFOx_oAY.; SUB=_2A25w1ilDDeRhGeNI6lUY-S7PyTmIHXVQOLcLrDV6PUJbktANLUf8kW1NSI-paC65V7mkcuupZWCjswxWCukefKzr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5j9J.kp46xkmGbvkz_UWpH5JpX5K-hUgL.Fo-ceKM41K50eo-2dJLoIEBLxKBLB.2L1hnLxKqL1h-L1K-LxK-L12BLB.qLxK-L1K5L1-zt; SUHB=0A0Jgn_8d-SKhl; SSOLoginState=1574066451; MLOGIN=1; _T_WM=67650424623; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E5%25BE%25B7%25E5%259B%25BD'
}
url = 'https://weibo.cn/search/mblog?' + urlencode(data)
print(url)
response = requests.get(url, headers=headers)
if response.status_code == 200:
    print(response.text)
    # pprint.pprint(response.json())
