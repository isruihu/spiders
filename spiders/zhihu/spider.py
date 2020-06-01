#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/29 Fri
# TIME: 22:46:43
# DESCRIPTION:知乎爬虫
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ROOT)

import requests
from zhihu import Zhihu
from utils import CookiePool
from utils import write_html



def zhihu_spider():
    url = 'https://www.zhihu.com/question/61170968'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br', # 加上这一行会乱码
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': r'https://www.zhihu.com/signin?next=%2F',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }
    cookie_list = CookiePool.get_cookies(Zhihu.cookie_table_name)
    cookie = cookie_list[0][1]
    headers['cookie'] = cookie
    response = requests.get(url, headers=headers)
    # print(response.content)
    write_html(response)


if __name__ == "__main__":
    zhihu_spider()