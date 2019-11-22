#!/usr/bin/env python
# encoding: utf-8

"""
@author: Wayne
@contact: wangye.hope@gmail.com
@software: PyCharm
@file: weibo_comments_m_weibo_cn.py
@time: 2019/11/18 16:54
"""

import csv
import datetime
import os
import random
import re
import shutil
import time
from urllib.parse import urlencode

import math
import requests
from lxml import etree

requests.packages.urllib3.disable_warnings()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': '''_T_WM=79690937411; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fm.weibo.cn%2Fcomments%2Fhotflow%3Fid%3D4417231498819866%26mid%3D4417231498819866%26max_id_type%3D0%26max_id%3D139250517984056; SCF=Av3drcZ8yVY2VVOSyBGTQaWu2qSjzM6qrCgXTMir-D-mRlsC-zLYQX2YXEIMwM2TaakN40_vD13l_N05rI9IXNQ.; SUB=_2A25w0jbfDeRhGeNI6lUY-S7PyTmIHXVQPVqXrDV6PUJbktANLXTCkW1NSI-paCyhcBD_UmW54xlyUHL5vlYFhWaF; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5j9J.kp46xkmGbvkz_UWpH5JpX5K-hUgL.Fo-ceKM41K50eo-2dJLoIEBLxKBLB.2L1hnLxKqL1h-L1K-LxK-L12BLB.qLxK-L1K5L1-zt; SUHB=0KAxUVcV9XkdWz; SSOLoginState=1574323855; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4417231498819866%26luicode%3D20000061%26lfid%3D4417231498819866'''
}


class WeiboCommentScrapy:  # (threading.Thread):
    def __init__(self, wid, keyword):
        global headers
        # threading.Thread.__init__(self)
        self.headers = headers
        self.result_headers = [
            '评论者主页',
            '评论者昵称',
            '评论者性别',
            '评论者所在地',
            '评论者微博数',
            '评论者关注数',
            '评论者粉丝数',
            '评论内容',
            '评论获赞数',
            '评论发布时间',
        ]
        if not os.path.exists('comment'):
            os.mkdir('comment')
        self.wid = wid
        self.keyword = keyword
        self.run()

    def parse_time(self, publish_time):
        publish_time = publish_time.split('来自')[0]
        if '刚刚' in publish_time:
            publish_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        elif '分钟' in publish_time:
            minute = publish_time[:publish_time.find('分钟')]
            minute = datetime.timedelta(minutes=int(minute))
            publish_time = (datetime.datetime.now() -
                            minute).strftime('%Y-%m-%d %H:%M')
        elif '今天' in publish_time:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            time = publish_time[3:]
            publish_time = today + ' ' + time
        elif '月' in publish_time:
            year = datetime.datetime.now().strftime('%Y')
            month = publish_time[0:2]
            day = publish_time[3:5]
            time = publish_time[7:12]
            publish_time = year + '-' + month + '-' + day + ' ' + time
        else:
            publish_time = publish_time[:16]
        return publish_time

    def getPublisherInfo(self, url):
        res = requests.get(url=url, headers=self.headers, verify=False)
        html = etree.HTML(res.text.encode('utf-8'))
        if not html:
            print(res.status_code, '找不到publish info')
            return None, None, None, None, None, None
        head = html.xpath("//div[@class='ut']/span[1]")[0]
        head = head.xpath('string(.)')[:-3].strip()
        key_index = head.index("/")
        nick_name = head[0:key_index - 2]
        sex = head[key_index - 1:key_index]
        location = head[key_index + 1:]

        footer = html.xpath("//div[@class='tip2']")[0]
        weibo_num = footer.xpath("./span[1]/text()")[0]
        weibo_num = weibo_num[3:-1]
        following_num = footer.xpath("./a[1]/text()")[0]
        following_num = following_num[3:-1]
        follows_num = footer.xpath("./a[2]/text()")[0]
        follows_num = follows_num[3:-1]
        print(nick_name, sex, location, weibo_num, following_num, follows_num)
        return nick_name, sex, location, weibo_num, following_num, follows_num

    def get_one_comment_struct(self, comment):
        # xpath 中下标从 1 开始
        user_url = "https://weibo.cn/{}".format(comment.xpath(".//a[1]/@href")[0])

        content = comment.xpath(".//span[@class='ctt']/text()")
        # '回复' 或者只 @ 人
        if '回复' in content or len(content) == 0:
            test = comment.xpath(".//span[@class='ctt']")
            content = test[0].xpath('string(.)').strip()

            # 以表情包开头造成的 content == 0,文字没有被子标签包裹
            if len(content) == 0:
                content = comment.xpath('string(.)').strip()
                content = content[content.index(':') + 1:]
        else:
            content = content[0]

        praisedNum = comment.xpath(".//span[@class='cc'][1]/a/text()")[0]
        praisedNum = praisedNum[2:praisedNum.rindex(']')]
        publish_time = comment.xpath(".//span[@class='ct']/text()")[0]
        publish_time = self.parse_time(publish_time)
        nickName, sex, location, weiboNum, followingNum, followsNum = self.getPublisherInfo(url=user_url)

        return [user_url, nickName, sex, location, weiboNum, followingNum, followsNum, content, praisedNum,
                publish_time]

    def write_to_csv(self, result, is_header=False):
        save_dir = f'comment/{self.keyword}'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        with open(f'{save_dir}/{self.wid}.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if is_header:
                writer.writerows([self.result_headers])
            writer.writerows(result)
        print(f'已成功将{len(result)}条评论写入comment/{self.keyword}/{self.wid}.csv中')

    def run(self):
        print(self.wid, self.headers)
        res = requests.get('https://weibo.cn/comment/' + self.wid, headers=self.headers, verify=False)
        comment_nums_pattern = re.findall("评论\[.*?\]", res.text)
        if comment_nums_pattern:
            comment_num = comment_nums_pattern[0]
            comment_num = int(comment_num[3:len(comment_num) - 1])
            print(f'comment num: {comment_num}')
            pageNum = math.ceil(comment_num / 10)
            print(f'page num: {pageNum}')
            for page in range(pageNum):
                result = []
                res = requests.get(f'https://weibo.cn/comment/{self.wid}?page={page + 1}', headers=self.headers,
                                   verify=False)
                html = etree.HTML(res.text.encode('utf-8'))
                if not html:
                    print(res.status_code, '找不到page num')
                    return None
                comments = html.xpath("/html/body/div[starts-with(@id,'C')]")
                print(f'第{page + 1}/{pageNum}页')
                for i in range(len(comments)):
                    result.append(self.get_one_comment_struct(comments[i]))
                if page == 0:
                    self.write_to_csv(result, is_header=True)
                else:
                    self.write_to_csv(result, is_header=False)
                time.sleep(random.randint(5, 10))


if __name__ == "__main__":
    shutil.rmtree('comment')
    key_words = ['vivo nex 3', 'vivo NEX 3 隐藏式压感', 'NEX 3 压感按键',
                 'NEX 3 隐藏式', 'NEX 3 隐藏按键', 'NEX 3 隐藏式按键',
                 'NEX 3 无按键', 'NEX 3 压感', 'vivo NEX 3 压感', 'mate 30 Pro 音量',
                 '华为 mate 30 pro 音量', 'NEX 3 压感 无按键', 'NEX 3 压感',
                 '华为 MATE 30 PRO 音量调节', '华为 MATE 30 PRO 音量条']
    for kw in key_words:
        save_str = ''
        for page in range(1, 101):
            url = 'https://weibo.cn/search/mblog?' + urlencode({
                'hideSearchFrame': '',
                'keyword': kw,
                'page': page
            })
            print(url)
            response = requests.get(url, headers=headers)
            if response.status_code == 418:
                print('请求过于频繁, 请等会儿再试试')
            remove = lambda p, x: re.sub(p, '', x)
            response_text = remove(r'(<a.*?</a>)', response.text)
            response_text = remove(r'(<img.*?/>)', response_text)
            response_text = remove(r'(<span class="kt".*?/span>)', response_text)
            response_text = remove(r'(<br/>)', response_text)
            texts = re.findall(
                r'<span class="ctt">:(.*?)</span>', response_text, re.S
            )
            for i, text in enumerate(texts):
                print(i + 1, text.strip())
                save_str += text.strip() + '\n'
            comment_urls = re.findall(
                r'href="https://weibo.cn/comment/(.*?)\?uid', response.text
            )
            for i_url, comment_url in enumerate(comment_urls):
                print(f'第{i_url + 1}个url: {comment_url}')
                WeiboCommentScrapy(wid=comment_url[:9], keyword=kw)
                time.sleep(5)
        with open(f'comment/{kw}/weibo.txt', 'a+') as f:
            f.write(save_str)
