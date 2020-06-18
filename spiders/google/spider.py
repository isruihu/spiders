#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/06/03 Wed
# TIME: 22:27:14
# DESCRIPTION:谷歌搜索 爬虫
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ROOT)

from config import opt
from utils.cookies import CookiePool
from utils.proxy_pool import get_proxy_ip_multithread
from utils import write_html
from google import Google
import requests
from queue import Queue
import threading
import random
from copy import deepcopy
import time


user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    # 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    # 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'
]


def google_spider():
    url = 'https://www.google.com.hk/search?hl=Chinese&q={}&btnG=Search&gbv=10'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    # 生成任务队列
    task_queue = Queue()
    with open(os.path.join(os.path.dirname(__file__), 'resource/task.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            name = line.replace('\n', '')
            task_queue.put(name)
    
    cnt = 0
    while task_queue.empty() is not True:
        name = task_queue.get()
        _url = url.format(name)
        _headers = deepcopy(headers)
        _headers['user-agent'] = user_agent[random.randint(0, 5)]
        try:
            response = requests.get(_url, headers=_headers, timeout=10)
            time.sleep(random.randint(3, 12))
            with open(os.path.join(os.path.dirname(__file__), 'output/{}.html'.format(name)), 'w', encoding='utf-8') as f:
                f.write(response.text)
            cnt += 1
            print(cnt, _url)
        except:
            task_queue.put(name)
            print("Update task.txt...........")
            with open(os.path.join(os.path.dirname(__file__), 'resource/task.txt'), 'a') as f:
                # 清空原文件
                f.seek(0)
                f.truncate()
                # 写入新的任务
                while task_queue.empty() is False:
                    name =  task_queue.get()
                    f.write("{}\n".format(name))
            print("Update finish.")


if __name__ == "__main__":
    google_spider()