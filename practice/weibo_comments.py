#!/usr/bin/env python
# encoding: utf-8

"""
@author: Wayne
@contact: wangye.hope@gmail.com
@software: PyCharm
@file: weibo_comments.py
@time: 2019/11/18 16:54
"""

import base64
import json
import logging
import random
import re
import time
from binascii import b2a_hex
from urllib import parse
from urllib.parse import urlencode

import requests
import rsa
from fake_useragent import UserAgent

replace = lambda x: re.sub('(<a.*?</a>)', '', re.sub('(<span.*?</span>)', '', x))

keywords = ['vivo nex3']
kw = keywords[0]
ua = UserAgent(verify_ssl=False)


class Weibo:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        # 用户名进过base64加密
        self.su = base64.b64encode(self.user.encode()).decode()
        self.session = requests.session()
        self.session.get('https://login.sina.com.cn/signup/signin.php')

    def pre_log(self):
        # 预登陆，获取信息
        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_={}'.format(
            parse.quote(self.su), int(time.time() * 1000))
        try:
            res = self.session.get(url).text
            res = re.findall(r"({.*})", res)[0]
            self.res = json.loads(res)
            self.nonce = self.res["nonce"]
            self.pubkey = self.res["pubkey"]
            self.rsakv = self.res["rsakv"]
            self.servertime = self.res["servertime"]
            # print(self.nonce,'\n',self.pubkey,'\n',self.rsakv,'\n',self.servertime)
        except Exception as error:
            logging.error("WeiBoLogin pre_log error: %s", error)

    def get_sp(self):
        '''用rsa对明文密码进行加密，加密规则通过阅读js代码得知'''
        publickey = rsa.PublicKey(int(self.pubkey, 16), int('10001', 16))
        message = str(self.servertime) + '\t' + str(self.nonce) + '\n' + str(self.password)
        self.sp = rsa.encrypt(message.encode(), publickey)
        return b2a_hex(self.sp)

    def judge_login_success(self):
        data = {
            'entry': 'account',
            'gateway': '1',
            'from': 'null',
            'savestate': '30',
            'useticket': '0',
            'vsnf': '1',
            'su': self.su,
            'service': 'account',
            'servertime': self.servertime,
            'nonce': self.nonce,
            'pwencode': 'rsa2',
            'rsakv': self.rsakv,
            'sp': self.get_sp(),
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'prelt': random.randint(1, 100),
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'TEXT'
        }
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        json_data = self.session.post(url, data=data).json()

        # 判断post登录是否成功
        if json_data['retcode'] == '0':
            params = {
                'ticket': json_data['ticket'],
                'ssosavestate': int(time.time()),
                'callback': 'sinaSSOController.doCrossDomainCallBack',
                'scriptId': 'ssoscript0',
                'client': 'ssologin.js(v1.4.19)',
                '_': int(time.time() * 1000)
            }
            # 二次登录网页验证
            url = 'https://passport.weibo.com/wbsso/login'
            res = self.session.get(url, params=params)
            # print(res.text)
            json_data1 = json.loads(re.search(r'({"result":.*})', res.text).group())
            # 判断是否登录成功
            if json_data1['result'] is True:
                print(res.cookies)
                logging.warning('WeiBo login Successed: %s', json_data1)
                return True
            else:
                logging.warning('WeiBo login Faild: %s', json_data1)
                return False
        else:
            logging.warning('WeiBo login Successed: %s', json_data)
            return True

    def login(self):
        data = {
            'entry': 'account',
            'gateway': '1',
            'from': 'null',
            'savestate': '30',
            'useticket': '0',
            'vsnf': '1',
            'su': self.su,
            'service': 'account',
            'servertime': self.servertime,
            'nonce': self.nonce,
            'pwencode': 'rsa2',
            'rsakv': self.rsakv,
            'sp': self.get_sp(),
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'prelt': random.randint(1, 100),
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'TEXT'
        }

        # 验证码
        if self.res["showpin"] == 1:
            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), self.res["pcid"])
            with open("captcha.jpg", "wb") as file_out:
                file_out.write(self.session.get(url).content)
            code = input("请输入验证码:")
            data["pcid"] = self.res["pcid"]
            data["door"] = code

        self.judge_login_success()

    def main(self):
        self.pre_log()
        self.login()


user = '13267080069'
password = 'haliluya314159'
weib = Weibo(user, password)
weib.main()
print('weibo login: ', weib.judge_login_success())

weibo_params = {
    'containerid': '100103type=1&q=vivo nex3',
    'page_type': 'searchall',
    'page': 1
}

weibo_headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    # 'set-cookie': login_success_response.headers['set-cookie']
    # 'cookies': 'ALF=1576640241; SCF=Av3drcZ8yVY2VVOSyBGTQaWu2qSjzM6qrCgXTMir-D-mBGQDmoKY8D4_AKU8o1mKXpxIxSfgou1P68inFOx_oAY.; SUB=_2A25w1ilDDeRhGeNI6lUY-S7PyTmIHXVQOLcLrDV6PUJbktANLUf8kW1NSI-paC65V7mkcuupZWCjswxWCukefKzr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5j9J.kp46xkmGbvkz_UWpH5JpX5K-hUgL.Fo-ceKM41K50eo-2dJLoIEBLxKBLB.2L1hnLxKqL1h-L1K-LxK-L12BLB.qLxK-L1K5L1-zt; SUHB=0A0Jgn_8d-SKhl; SSOLoginState=1574066451; MLOGIN=1; _T_WM=67650424623; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E5%25BE%25B7%25E5%259B%25BD'
}
weibo_url = 'https://m.weibo.cn/api/container/getIndex?' + urlencode(weibo_params)
print(weibo_url)

weibo_response = weib.session.get(weibo_url, headers=weibo_headers)
if weibo_response.status_code == 200:
    weibo_content = weibo_response.json()
    if weibo_content['ok'] == 1:
        cards = weibo_content['data']['cards']
        for card in cards:
            if 'card_type_name' in card and card['card_type_name'] == '微博':
                blog = card['mblog']
                text = replace(blog['text'])
                print('1: ' + text)
                comments_url = 'https://m.weibo.cn/comments/hotflow?'
                comments_params = {
                    'id': blog['id'],
                    'mid': blog['mid'],
                    'max_id_type': 0
                }
                comment_headers = weibo_headers.copy()
                comment_headers['referer'] = 'https://m.weibo.cn/detail/' + blog['id']
                while True:
                    time.sleep(2)
                    print(comments_url + urlencode(comments_params))
                    comments_response = weib.session.get(comments_url + urlencode(comments_params), headers=comment_headers)
                    if comments_response.status_code == 200:
                        try:
                            comments_content = comments_response.json()
                            if comments_content['ok'] == 1:
                                comments_data = comments_content['data']
                                # print('--------------------------')
                                # print(comments_url)
                                comments = comments_data['data']
                                for comment in comments:
                                    # print(comment.keys())
                                    comment_text = replace(comment['text'])
                                    print('2: ' + comment_text)
                                    sub_comments = comment['comments']
                                    if sub_comments != False:
                                        # pprint.pprint(comment)
                                        # print(sub_comments)
                                        for sub_comment in sub_comments:
                                            # print(sub_comment.keys())
                                            sub_comment_text = replace(sub_comment['text'])
                                            print('3: ' + sub_comment_text)
                                if 'max_id' in comments_data:
                                    comments_params['max_id'] = comments_data['max_id']
                                    comments = comments_data['data']
                                else:
                                    break
                        except Exception as e:
                            print('不能转为json格式')
                            time.sleep(5)
                            import time

                            # print(comments_response.text)
