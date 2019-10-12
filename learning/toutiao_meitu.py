#!/usr/bin/env python
# encoding: utf-8

"""
@author: Wayne
@contact: wangye.hope@gmail.com
@software: PyCharm
@file: toutiao_meitu
@time: 2019/10/10 15:59
"""

import json
from urllib.parse import urlencode

import codecs
import requests


def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1
    }
    url = r'https://www.toutiao.com/api/search/content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except requests.exceptions.RequestException:
        print('请求索引页出错')
        return None


def parse_page_index(html):
    data = json.loads(html)
    # print(data)
    if data and 'data' in data.keys():
        # print(data.get('data'))
        for item in data.get('data'):
            if 'article_url' in item:
                yield item.get('article_url')


def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except requests.exceptions.RequestException:
        print('请求详情页出错', url)
        return None


def parse_page_detail(html):
    pass


def main():
    html = get_page_index(0, '美女')
    # print(html)
    for url in parse_page_index(html):
        html = get_page_detail(url)


if __name__ == '__main__':
    # main()
    s = u'&quot;\u003Cdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002Fa8089432a13c4ad5a9875290441f8e4d\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;386\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cp class&#x3D;\&quot;ql-align-justify\&quot;\u003E优雅高贵，冷艳美女\u003C\u002Fp\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp3.pstatp.com\u002Flarge\u002Fpgc-image\u002Fee3a042a5d4c4ddfa8a81b195fafa183\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;385\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp3.pstatp.com\u002Flarge\u002Fpgc-image\u002Fe7f4b79aacac4b20a59bea59d234d9a2\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;871\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002Ff0feeef346c4431db68ce7d9cc7fa7db\&quot; img_width&#x3D;\&quot;524\&quot; img_height&#x3D;\&quot;788\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp3.pstatp.com\u002Flarge\u002Fpgc-image\u002F681bed763f0f489cb913f8463855aa7b\&quot; img_width&#x3D;\&quot;573\&quot; img_height&#x3D;\&quot;860\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F94b7285a757a45a2b7a7cf8ea3c616a9\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;386\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002Fe7e358e8446544eb84c319866d189b6b\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;871\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F4ca2b8f0bc544f7d8af140469aa754fa\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;386\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp3.pstatp.com\u002Flarge\u002Fpgc-image\u002F0fc48448ec9743f6b4e91cd979cdbd19\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;874\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F0719fe99350b45ed81e6d6b770d6c3e6\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;387\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F168160767d084a3ba9f6e4d13f4eeb67\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;871\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F63dff403d6364e22a85acf6ecde372ec\&quot; img_width&#x3D;\&quot;558\&quot; img_height&#x3D;\&quot;841\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F06f4ba817fd74e57895bfeaa92add36a\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;871\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002Fc34eb0e285bf481e85adf4deac58fb63\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;386\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp3.pstatp.com\u002Flarge\u002Fpgc-image\u002F621ccb0fbfc74dd5aeac9c63dee7b902\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;386\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002Fd165a93546cc4147b7ffcb36a4c16e68\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;386\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002Ff6207db9897f4b93ac919629335d41a5\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;872\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F8e41f2986c3b402fa0b2196986234439\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;871\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp3.pstatp.com\u002Flarge\u002Fpgc-image\u002Fb41b314eb3784a8dab4791b5f3c61490\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;871\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F01cdc92df317423c96ab7d2a90a03b61\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;872\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F34ff1a8c7c684354baceae7ed67f3688\&quot; img_width&#x3D;\&quot;580\&quot; img_height&#x3D;\&quot;871\&quot; alt&#x3D;\&quot;气质美女：优雅高贵，冷艳美女\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E&quot;'
    print(codecs.decode(s,'unicode_escape'))
