#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/06/17 Wed
# TIME: 12:59:37
# DESCRIPTION: 英伟财经
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ROOT)

from utils import get_proxy_ip_multithread, test_proxy_ip
from config import opt
from queue import Queue
import requests
from requests import ConnectionError, ConnectTimeout, ReadTimeout
import threading
from threading import Lock
import time
import random

test_url = 'https://cn.investing.com/equities/microsoft-corp-ar'


def investing_spider():
    url = 'https://cn.investing.com/equities/{}-company-profile'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    task_queue = Queue()
    with open(os.path.join(os.path.dirname(__file__), 'resource/task.txt'), 
                'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            country, company = line.split()
            task_queue.put((country, company))
    
    # 是否使用多线程
    if opt.use_proxy:
        proxy_list = []
        # 多线程获取代理ip，速度更快
        proxy_ip = get_proxy_ip_multithread(test_url, threading_num=10, headers=headers) 
        proxy_list.append(proxy_ip)

    lock = Lock()
    def targart():
        cnt = 0
        while task_queue.empty() is False:
            # 文件控制线程结束
            with open(os.path.join(os.path.dirname(__file__), 'thread_controller'), 'r', encoding='utf-8') as f:
                if len(f.readlines()) == 0:
                    print("{} has stopped.".format(threading.currentThread().name))
                    raise RuntimeError("Stop {}".format(threading.currentThread().name))

            country, company = task_queue.get()
            _url = url.format(company)
            if opt.use_proxy:
                while(True):
                    try:
                        proxy_ip = proxy_list[0]
                        break
                    except IndexError:
                        continue
                proxies = {
                    "http": "http://{}".format(proxy_ip),
                    "https": "https://{}".format(proxy_ip)
                }
            else:
                proxies = None
            
            error_time = 0
            for _ in range(3):
                try:
                    response = requests.get(_url, headers=headers, proxies=proxies, timeout=10)
                    if response.status_code != 200:
                        raise RuntimeError('IP has been baned!!')
                    else:
                        cnt += 1
                        time.sleep(random.uniform(1, 1.5))
                        print("{} {} {}".format(threading.currentThread().name, cnt, _url))
                        break
                except (RuntimeError, ConnectionError, ConnectTimeout, ReadTimeout):
                    error_time += 1
                    if error_time < 3:
                        continue
                    else:
                        # 如果出错了，就把取出的任务放回队列
                        task_queue.put((country, company))
                        if opt.use_proxy:
                            print("proxy failed. Getting proxy ip again.")
                            # 重新获取一个代理ip
                            lock.acquire() # TODO: 虽然加了锁，还是无法保证多个线程只重新获取一次
                            proxy_list.pop(0)
                            proxy_ip = get_proxy_ip_multithread(test_url, threading_num=10, headers=headers) 
                            proxy_list.append(proxy_ip)
                            lock.release()
                            continue
                        else:
                            raise RuntimeError("网络错误.")
            with open(os.path.join(os.path.dirname(__file__), 'output/{}_{}.html'.format(country, company)), 'w', encoding='utf-8') as f:
                f.write(response.text)
    
    threadings = []
    for _ in range(1):
        t = threading.Thread(target=targart)
        threadings.append(t)
    for t in threadings:
        t.setDaemon(True)
        t.start()
    for t in threadings:
        t.join()
    
    # 子线程全部结束，将task_queue更新到文件
    print("Update task.txt...........")
    with open(os.path.join(os.path.dirname(__file__), 'resource/task.txt'), 'a', encoding='utf-8') as f:
        # 清空原文件
        f.seek(0)
        f.truncate()
         # 写入新的任务
        while task_queue.empty() is False:
            country, company =  task_queue.get()
            f.write("{} {}\n".format(country, company))
    print("Update finish.")       


if __name__ == "__main__":
    investing_spider()