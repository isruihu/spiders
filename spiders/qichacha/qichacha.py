#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/19 Tue
# TIME: 16:25:12
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ROOT)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import opt
from utils.login import LoginBaseModule, get_tracks, move_to_gap
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import InvalidSelectorException, TimeoutException
import time
import numpy as np


class Qichacha(LoginBaseModule):
    """
    企查查模拟登录
    """
    cookie_table_name = 'qcc'
    test_url = 'http://www.qcc.com/'

    def __init__(self, username, password):
        headless = False # 是否开启无头模式
        super(Qichacha, self).__init__(headless=headless)
        
        self.login_url = 'https://www.qcc.com/user_login'
        self.username = username
        self.password = password

    def login(self):
        self.browser.get(self.login_url)
        time.sleep(5)
        # 切换到密码登录
        normal_login = self.browser_wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, '//a[@id="normalLogin"]'))
        )
        normal_login.click()
        # # 输入账号
        self.browser.find_element_by_id('nameNormal').send_keys(self.username)
        # # 输入密码
        self.browser.find_element_by_id('pwdNormal').send_keys(self.password)
        # 拖动滑块
        slider = self.browser_wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@class="nc_iconfont btn_slide"]'))
        )
        tracks = get_tracks(distance=340)
        move_to_gap(self.browser ,slider=slider, tracks=tracks)
        # 点击登录
        self.browser.find_element_by_css_selector('button.btn.btn-primary.btn-block.m-t-md.login-btn').click()
        time.sleep(5)

        self.browser.get('https://www.qcc.com')
        time.sleep(5)
        # 找登录后的用户元素
        try:
            self.browser_wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//li[@class="dropdown user-drop"]'))
            )
            cookies = self.browser.get_cookies()
            print("{} login successfully.".format(self.username))
            print(cookies)
        except TimeoutException as e:
            print(e)
            cookies = False
        return cookies


def qcc_cookie_check(response):
    """
    检查cookie是否失效
    html: 带cookie访问返回的页面
    如果cookie过期，企查查会跳转到登录页面，判断是否有登录页面的元素即可
    """
    from lxml import etree

    # selector = etree.HTML(response.text)
    selector = etree.HTML(response.text)
    login_tab = selector.xpath('//div[@class="login-tab col3"]')
    if len(login_tab) == 3:
        # print("This cookie has expired.")
        return False
    return True
    

if __name__ == "__main__":
    qcc = Qichacha('17373229849', '0.123456')
    qcc.login()