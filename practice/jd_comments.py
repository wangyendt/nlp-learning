# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: wang121ye
# datetime: 2019/10/17 17:01
# software: PyCharm

import json
import re
import time
from urllib.parse import urlencode

import pandas as pd
import requests
from fake_useragent import UserAgent


class Spider:
    def __init__(self, url_base, data, headers, *args, **kwargs):
        self.url_base = url_base
        self.data = data
        self._update_url()
        self.user_agent = UserAgent(verify_ssl=False)
        self.headers = headers
        self.response_parser = kwargs['parse_response']
        self.num_pages_getter = kwargs['page_nums_getter']
        self.retry = kwargs['retry']
        if 'page_info' in kwargs:
            self.page_keyword = kwargs['page_info']['page_keyword']
            self.max_page_keyword = kwargs['page_info']['max_page_keyword']
            if 'page_url' in kwargs['page_info']:
                self.url_page = kwargs['page_info']['page_url']
            else:
                self.url_page = self.url

    def _update_url(self):
        self.url = self.url_base + urlencode(self.data)

    def get_num_pages(self):
        self.headers['User-Agent'] = self.user_agent.random
        response = requests.get(self.url_page, headers=self.headers)
        if response.status_code == 200:
            return self.num_pages_getter(response, self.max_page_keyword)

    def get_single_page_info(self, page):
        df = pd.DataFrame()
        self.data[self.page_keyword] = page
        self._update_url()
        self.headers['User-Agent'] = self.user_agent.chrome
        cnt = 0
        while cnt < self.retry:
            cnt += 1
            time.sleep(0.2)
            try:
                response = requests.get(self.url, headers=self.headers)
                if response.status_code == 200:
                    for res in self.response_parser(response):
                        df = df.append(res, ignore_index=True)
                    return df
            except:
                print(f'正在重试第{page}页, 第{cnt}次')
                continue
            finally:
                print(f'正在爬取第{page}页...')

    def work(self, save_path):
        page_nums = self.get_num_pages()
        print(f'共有{page_nums}页')
        df_save = pd.DataFrame()
        for i in range(1, 1 + page_nums):
            df_save = df_save.append(self.get_single_page_info(i))
        df_save.to_excel(save_path, index=False)


if __name__ == '__main__':
    target = {
        # 'vivo-nex3': '100007988984',
        # 'vivo-nex3-5g': '100007988988',
        # 'vivo-iqoo-pro': '100007612396',
        # 'vivo-iqoo-pro-5g': '100007411764',
        # 'huawei-p30-pro': '100008384328',
        # 'huawei-p30-pro-union': '100004788075',
        'vivo-iqoo-pro': '100007612396',
        'vivo-iqoo-pro-5g(8+128)': '100007411764',
        'vivo-iqoo(8+256)':'100002425257',
        'vivo-iqoo-neo(6+128)': '100005179183',
        'vivo-iqoo-5g':'57984427611',
        'vivo-iqoo-pro-5g':'57168056742',
    }

    url_base = 'https://sclub.jd.com/comment/productPageComments.action?'
    data = {
        'callback': 'fetchJSON_comment98vv1437',
        'productId': '100007411764',
        'score': 0,
        'sortType': 5,
        'page': 0,
        'pageSize': 10,
        'isShadowSku': 0,
        'fold': 1
    }
    headers = {
        'Referer': 'https://item.jd.com/100007411764.html#comment',
        'Sec-Fetch-Mode': 'no-cors',
    }
    useful_fields = ['nickname', 'content', 'creationTime', 'mobileVersion', 'referenceName', 'referenceTime',
                     'score', ]


    def response2num_pages(response, page_keyword):
        pattern = re.compile(r'^.*?\((.*)\).*?$', re.S)
        js = json.loads(re.findall(pattern, response.text)[0])
        return int(js[page_keyword])


    def response2json(response):
        pattern = re.compile(r'^.*?\((.*)\).*?$', re.S)
        js = json.loads(re.findall(pattern, response.text)[0])
        # import pprint
        # pprint.pprint(js)
        # pprint.pprint(js['comments'])
        for j in js['comments']:
            yield {
                p: j[p] for p in useful_fields
            }


    params = {
        'url_base': url_base,
        'data': data,
        'headers': headers,
        'retry': 10,
        'parse_response': response2json,
        'page_nums_getter': response2num_pages,
        'page_info': {'page_keyword': 'page', 'max_page_keyword': 'maxPage'}
    }

    for k, v in target.items():
        print(f'正在爬取{k}的评论...')
        path = f'data/jd-comments_{k}.xlsx'
        params['data']['productId'] = v
        params['headers']['Referer'] = f'https://item.jd.com/{v}.html'
        spider = Spider(**params)
        spider.work(path)
