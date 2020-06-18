#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/20 Wed
# TIME: 16:33:47
# DESCRIPTION: Ip代理池
import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import warnings
import requests
from requests import ConnectionError, ConnectTimeout, ReadTimeout
from requests.exceptions import ProxyError
from html_test import write_html
from config import opt
import threading
import time
import ctypes


SERVER = opt.ip_proxy_server
INVALID_THRESHOLD = 10


class ProxyPool:
    """ip代理池相关操作"""
    @staticmethod
    def get_proxy():
        proxy_ip = requests.get("{}/get".format(SERVER), timeout=5)
        return proxy_ip

    @staticmethod
    def delete_proxy(proxy_ip):
        requests.get("{}/delete/?proxy={}".format(SERVER, proxy_ip))


def test_proxy_ip(proxy_ip, test_url, headers=None):
    """
    测试代理ip有效性
    proxy_ip: 代理ip
    test_url: 测试地址
    """
    status_code = None
    for _ in range(3):
        try:
            proxies = {
                "http": "http://{}".format(proxy_ip),
                "https:": "https://{}".format(proxy_ip)
            }
            res = requests.get(url=test_url, timeout=3, proxies=proxies, headers=headers)
            write_html(res)
            status_code = res.status_code
            if res.status_code == 200:
                print("{} is VALID!".format(proxy_ip))
                return True
        except (ProxyError, ConnectTimeout, ConnectionError, ReadTimeout) as e:
            # print(e)
            continue
    print("{} is invaild. {}".format(proxy_ip, status_code))
    return False


def get_proxy_ip(test_url, headers=None):
    """
    获取一个有效代理ip(循环测试代理ip，直到找到一个有效代理)
    """
    invalid = 0
    while True:
        # 无效ip数量
        try:
            proxy_ip = ProxyPool.get_proxy()
            proxy_ip = proxy_ip.text
            # 删除代理ip
            ProxyPool.delete_proxy(proxy_ip)
        except (ConnectionError, ConnectTimeout, ReadTimeout):
            raise RuntimeError("Failed to connect to the Proxy Server.")
        # 测试代理ip是否有效
        try:
            if test_proxy_ip(proxy_ip, test_url, headers=headers):
                return proxy_ip
            else: # 状态码 != 200
                invalid += 1
        except (ConnectionError, ConnectTimeout): # 连接url失败
            invalid += 1
        if invalid % INVALID_THRESHOLD == 0:
            warnings.warn("Thera are {} invalid proxy ips getted continuously，it's better to refresh the Proxy Pool.".format(INVALID_THRESHOLD))
        

class thread_with_exception(threading.Thread): 
    """带异常的线程"""
    def __init__(self, proxy_ip:list, test_url, headers=None): 
        threading.Thread.__init__(self) 
        self.proxy_ip = proxy_ip
        self.test_url = test_url
        self.headers = headers

    def run(self): 
        # target function of the thread class 
        ip = get_proxy_ip(self.test_url, headers=self.headers)
        self.proxy_ip.append(ip)
        # while True:
        #     print("{} still running.".format(threading.currentThread().name))

    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def raise_exception(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)  


def get_proxy_ip_multithread(test_url, threading_num=5, headers=None):
    """
    多线程获取代理ip
    test_url: 测试代理ip有效性的url
    threading_num: 多线程数量
    """
    
    proxy_ip = []

    threadings = []
    # 创建线程池
    for _ in range(threading_num):
        t = thread_with_exception(proxy_ip, test_url)
        threadings.append(t)
    # 开启线程池
    for t in threadings:
        t.setDaemon(True)  # 守护式线程，主线程结束则子线程全部结束
        time.sleep(1) # 间隔开启线程，保证每个线程获取到的ip不同，提高效率
        t.start() 
    # for t in threadings:
        # t.join()

    while True:
        if len(proxy_ip) > 0: 
            # 结束所有线程
            for t in threadings:
                # print("{}  stop.".format(t.name))
                t.raise_exception()
            print(proxy_ip)
            return proxy_ip[0]


if __name__ == "__main__":
    get_proxy_ip_multithread('https://cn.investing.com/', 10)
