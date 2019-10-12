#!/usr/bin/env python
# encoding: utf-8

"""
@author: Wayne
@contact: wangye.hope@gmail.com
@software: PyCharm
@file: maoyan
@time: 2019/10/10 14:44
"""

import json
import os
import re
from multiprocessing import Pool

import requests


def get_one_page(url):
    try:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        response = requests.get(url, headers=header)
        print(response)
        if response.status_code == 200:
            return response.text
        return None
    except requests.exceptions.RequestException:
        print('request exception')
        return None


def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         r'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         r'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    # print(items)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def clear_file():
    if os.path.exists(result_path):
        os.remove(result_path)


def write_to_file(save_path, content):
    with open(save_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(params):
    save_path, offset = params
    url = r'https://maoyan.com/board/4?offset=' + str(offset)
    print(url)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(save_path, item)


if __name__ == '__main__':
    result_path = 'maoyan_result.txt'
    clear_file()
    # for i in range(10):
    #     main(i * 10)
    pool = Pool()
    pool.map(main, [(result_path, i * 10) for i in range(10)])
