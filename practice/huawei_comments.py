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

import pandas as pd
import requests

# from ndtpy.tools import *

comments_url = 'https://openapi.vmall.com/rms/comment/getCommentList.json?'


def get_page_number(url):
    data = {
        't': int(1000 * time.time()),
        'pid': '10086341244716',
        'pageNum': 1
    }
    header = {
        "Accept-Encoding": "gzip, deflate",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }

    while True:
        time.sleep(1)
        response = requests.get(url + urlencode(data), headers=header)
        response.encoding = 'utf-8'
        if response.json()['info'] == '成功':
            return int(response.json()['data']['page']['totalPage'])
        print(f'正在重试爬取页数...')


def get_one_page_comments(url: str, page: int) -> str:
    data = {
        't': int(1000 * time.time()),
        'pid': '10086341244716',
        'pageNum': page
    }
    header = {
        "Accept-Encoding": "gzip, deflate",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }

    while True:
        time.sleep(1)
        response = requests.get(url + urlencode(data), headers=header)
        response.encoding = 'utf-8'
        print(f'正在爬取第{page}页...')
        if response.json()['info'] == '成功':
            # pprint.pprint(response.json())
            return response.json()['data']['comments']
        print(f'正在重试第{page}页')


def parse_one_page_comments(url: str, page: int):
    js = get_one_page_comments(url, page)
    for j in js:
        yield {
            p: j[p] for p in [
                'commentLevel', 'content', 'creationTime',
                'gradeCode', 'likes', 'score', 'skuAttrs', 'skuName',
                'userName'
            ]
        }
    # pprint.pprint(js)


def main():
    df = pd.DataFrame()
    writer = pd.ExcelWriter('huawei-comments.xlsx', engine='openpyxl', mode='w')
    page_nums = get_page_number(comments_url)
    use_header = True
    for page in range(page_nums):
        start_row = len(df)
        df = pd.DataFrame()
        for res in parse_one_page_comments(comments_url, page + 1):
            df = df.append(res, ignore_index=True)
        df.index = range(start_row, start_row + len(df))
        df.to_excel(writer, startrow=start_row, header=use_header)
        use_header = False
        writer.save()


if __name__ == '__main__':
    main()
