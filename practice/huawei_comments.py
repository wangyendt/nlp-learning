#!/usr/bin/env python
# encoding: utf-8

"""
@author: Wayne
@contact: wangye.hope@gmail.com
@software: PyCharm
@file: huawei_comments
@time: 2019/10/12 17:36
"""

import time
from urllib.parse import urlencode

import requests

url = 'https://openapi.vmall.com/rms/comment/getCommentList.json?'
data = {
    't': int(1000 * time.time())
}
header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'CsrfToken': 'A2D2187E0F046FFDC41246652DD3953ADF137634D09598EC',
    'Origin': 'https://www.vmall.com',
    'Referer': 'https://www.vmall.com/product/10086341244716.html',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
form_data = {
    'pid': 10086341244716,
    'gbomCode': '',
    'type': 0,
    'extraType': 1,
    'pageSize': 10,
    'pageNum': 1
}
print(url + urlencode(data))
with requests.Session() as sess:
    sess.options(url + urlencode(data),headers= header)
    response = sess.post(url + urlencode(data), headers=header, data=form_data)

print(response.text)
