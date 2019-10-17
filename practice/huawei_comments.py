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
from multiprocessing import Pool
from urllib.parse import urlencode

import pandas as pd
import requests
from fake_useragent import UserAgent

comments_url = 'https://openapi.vmall.com/rms/comment/getCommentList.json?'

global_vars = {
    'num_pages': 0,
    'ua': UserAgent(verify_ssl=False)
}


def get_page_number(url):
    data = {
        't': int(1000 * time.time()),
        'pid': '10086341244716',
        'pageNum': 1
    }
    header = {
        "Accept-Encoding": "gzip, deflate",
        'User-Agent': global_vars['ua'].chrome
    }

    while True:
        time.sleep(0.2)
        try:
            response = requests.get(url + urlencode(data), headers=header)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                if response.json()['info'] == '成功':
                    return int(response.json()['data']['page']['totalPage'])
        except:
            continue
        finally:
            print(f'正在重试爬取页数...')


def get_one_page_comments(url: str, page: int) -> str:
    data = {
        't': int(1000 * time.time()),
        'pid': '10086341244716',
        'pageNum': page
    }
    header = {
        "Accept-Encoding": "gzip, deflate",
        'User-Agent': global_vars['ua'].random
    }

    while True:
        time.sleep(0.2)
        try:
            response = requests.get(url + urlencode(data), headers=header)
            response.encoding = 'utf-8'
            if response.json()['info'] == '成功':
                # pprint.pprint(response.json())
                return response.json()['data']['comments']
        except:
            print(f'正在重试第{page}页')
            continue
        finally:
            print(f'正在爬取第{page}页...')


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


def main(page):
    df = pd.DataFrame()
    for res in parse_one_page_comments(comments_url, page):
        df = df.append(res, ignore_index=True)
    return df


if __name__ == '__main__':
    global_vars['num_pages'] = page_nums = get_page_number(comments_url)
    pool = Pool()
    max_worker = 64
    n_tasks = page_nums // max_worker
    result = []
    print(global_vars['num_pages'])
    for i in range(n_tasks + 1):
        result += pool.imap(main, range(max_worker * i + 1, min(page_nums, max_worker * (i + 1)) + 1))
    df_save = pd.concat(result)
    df_save.to_excel('data/huawei-comments.xlsx', index=False)
