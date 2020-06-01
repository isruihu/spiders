#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/20 Wed
# TIME: 15:49:49
# DESCRIPTION: 企查查爬虫
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ROOT)

from utils import cookie2dict, cookie2str, write_html
from utils import CookiePool
from utils import get_proxy_ip, get_proxy_ip_multithread, test_proxy_ip
from config import opt
from qichacha import Qichacha, qcc_cookie_check
import requests
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout
import queue
from lxml import etree
import threading
from threading import Lock
import time
import random
from copy import deepcopy


def login():
    with open(os.path.join(os.path.dirname(__file__), 'resource/account.txt')) as f:
        accounts = [line.split() for line in f.readlines()]
    
    cookies= []
    for username, password in accounts:
        qcc = Qichacha(username, password)
        cookie = qcc.login()
        if cookie is False:
            print("{} login failed.".format(username))
        else:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
            cookies.append(cookie2str(cookie))
    # 将cookies存入cookie池
    CookiePool.insert_cookies(Qichacha.cookie_table_name, cookies)
    return cookies


def qcc_spider():
    url = 'https://www.qcc.com/company_ipoview?code={}&ajaxFlag=1&type=cgkg&p={}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',        
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://www.qcc.com/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }

    if opt.use_proxy:
        proxy_list = []
        # 多线程获取代理ip，速度更快
        proxy_ip = get_proxy_ip_multithread(Qichacha.test_url, threading_num=10) 
        proxy_list.append(proxy_ip)
    else:
        proxies = None

    # python 自带的 Queue 是线程安全的
    task_queue = queue.Queue()
    # 初始化任务队列
    with open(os.path.join(os.path.dirname(__file__), 'resource/task.txt'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            code, page = line.split()
            task_queue.put((code, int(page)))

    lock = Lock()
    def target(cookie_tuple):
        """
        多线程目标函数
        cookie_tuple: cookie池里的一条记录 (id, cookie)
        """
        _id, cookie = cookie_tuple
        cnt = 0
        while task_queue.empty() is not True:
            # 文件控制线程退出
            with open(os.path.join(os.path.dirname(__file__), 'thread_controller'), 'r', encoding='utf-8') as f:
                if len(f.readlines()) == 0:
                    print("{} has stopped.".format(threading.currentThread().name))
                    raise RuntimeError("Stop {}".format(threading.currentThread().name))

            # 领取任务
            code, page = task_queue.get()
            _url = url.format(code, page)
            _headers = deepcopy(headers)
            _headers['cookie'] = cookie
            # print("{} {}".format(threading.Thread().name, _headers))
            # 发出请求
            time.sleep(random.randint(1, 5)) # 请求一次休眠 3~8 秒
            if opt.use_proxy:
                c_t = 0
                while True:
                    # print(f"{threading.currentThread().name} {c_t}")
                    try:
                        while True:
                            try:
                                proxy_ip = proxy_list[0] # 在嵌套函数中可以修改父函数中可变参数(列表、字典等)的值
                                break
                            except IndexError:
                                continue
                        proxies = {
                            "http": "http://{}".format(proxy_ip),
                            "https:": "https://{}".format(proxy_ip)
                        }
                        response = requests.get(_url, headers=_headers, proxies=proxies, timeout=5)
                        # print("{} ".format(proxy_ip), end='')
                        break
                    except (ConnectionError, ConnectTimeout, ReadTimeout) as e: # 出现连接异常，有可能是代理失效，也可能是账号被限制了
                        print("111111111111111111111111111111111111111111111111111111111111111111111111111")
                        if test_proxy_ip(proxy_ip, Qichacha.test_url) is False: # 如果是代理失效了，则重新获取代理IP
                            print("proxy failed. Getting proxy ip again.")
                            # 重新获取一个代理ip
                            lock.acquire() # TODO: 虽然加了锁，还是无法保证多个线程只重新获取一次
                            proxy_list.pop(0)
                            proxy_ip = get_proxy_ip_multithread(Qichacha.test_url, threading_num=10) 
                            proxy_list.append(proxy_ip)
                            lock.release()
                            continue
                        else:  # 不是代理Ip的问题，应该是账号被限制了
                            c_t += 1 
                            if c_t <= 3:
                                continue
                            else:
                                print("账号被限制访问了!!!!!!!!")
                                raise e
            else:
                c_t = 0 # 请求错误次数，如果连续3次请求错误，则认为账号被限制了
                for _ in range(3):
                    try:
                        response = requests.get(_url, headers=_headers, timeout=10)
                    except (ConnectionError, ConnectTimeout, ReadTimeout) as e:
                        c_t += 1
                        if c_t < 3:
                            continue
                        else:
                            # 将取出的任务放回队列
                            task_queue.put((code, page))
                            print("账号被限制访问了!!!!!!!!!!!!!!!")
                            raise e
            # 检查cookie
            if qcc_cookie_check(response) == False:
                # 将取出的任务放回队列
                task_queue.put((code, page))
                # 从cookie池里删除这个过期cookie
                CookiePool.delete_cookies(Qichacha.cookie_table_name, _id)
                raise RuntimeError("This cookie has expired.")
            
            # 判断是否有下一页
            selector = etree.HTML(response.text)
            # 当前li的下一个li如果存在说明下一页存在
            res = selector.xpath('//li[@class="active"]/following-sibling::li[1]')
            next_page = True if len(res) > 0 else False
            # 生成新任务
            if next_page:
                task_queue.put((code, page+1))
            # 保存html文件
            with open(
                os.path.join(ROOT, 'spiders/qichacha/output/{}_{}.html'.format(code, page)
                ), 'w', encoding='utf-8'
            ) as f:
                f.write(response.text)
            cnt += 1
            # print("{} {} {}".format(threading.currentThread().name, cnt, _url))
            if cnt % 30 == 0:
                if opt.use_proxy:
                    print("{}\t{}\t{}\t{}".format(proxy_list[0], threading.currentThread().name, cnt, _url))
                else:
                    print("{}\t{}\t{}".format(threading.currentThread().name, cnt, _url))
                print("{} has already requested {} times, sleep 0.5 minutes.".format(threading.currentThread().name, cnt))
                time.sleep(30)

    # print(CookiePool.get_cookies('qcc'))
    cookie_list = CookiePool.get_cookies(Qichacha.cookie_table_name) # [(id, cookie), (), ...]
    if len(cookie_list) == 0:
        print("Cookie pool is empty, please get cookie first.")
        return 
    threadings = []
    for item in cookie_list:
        t = threading.Thread(target=target, args=(item,))
        threadings.append(t)
    for t in threadings:
        t.setDaemon(True) # 守护式线程
        t.start()
    for t in threadings:
        t.join()

    # 子线程全部结束，将task_queue更新到文件
    print("Update task.txt...........")
    with open(os.path.join(os.path.dirname(__file__), 'resource/task.txt'), 'a') as f:
        # 清空原文件
        f.seek(0)
        f.truncate()
         # 写入新的任务
        while task_queue.empty() is False:
            code, page =  task_queue.get()
            f.write("{} {}\n".format(code, page))
    print("Update finish.")       


if __name__ == "__main__":
    # CookiePool.delete_cookies(Qichacha.cookie_table_name, None)
    # login()
    qcc_spider()