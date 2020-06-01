#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/29 Fri
# TIME: 19:24:13
# DESCRIPTION:模拟知乎登录
import os 
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ROOT)

import time
from utils import LoginBaseModule
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class Zhihu(LoginBaseModule):
    """
    继承自LoginBaseModule抽象类，必须实现login()抽象方法
    """
    test_url = 'https://www.zhihu.com/'
    cookie_table_name = 'zhihu'

    def __init__(self, username, password):
        headless, imageless = False, False
        super(Zhihu, self).__init__(headless=headless, imageless=imageless)

        # self.login_url = r'https://www.zhihu.com/signin?next=%2F'
        self.login_url = 'https://account.dianping.com/login?redir=http://www.dianping.com'
        self.username = username
        self.password = password


    def login(self):
        self.browser.get(self.login_url)
        # time.sleep(5)
        # # 切换到用户名密码登录
        # self.browser_wait.until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@class="SignFlow-tab"]'))
        # ).click()
        # # 输入用户名
        # self.browser_wait.until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@class="SignFlow-account"]/descendant::input'))
        # ).send_keys(self.username)
        # # 输入密码
        # self.browser_wait.until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@class="SignFlow-password"]/descendant::input'))
        # ).send_keys(self.password)
        # # 点击登录按钮
        # time.sleep(2)
        # self.browser.find_element_by_css_selector("button.Button.SignFlow-submitButton.Button--primary.Button--blue").click()
        
        # time.sleep(5)
        # try:
        #     self.browser_wait.until(
        #         EC.presence_of_element_located((By.XPATH, '//div[@class="AppHeader-userInfo"]'))
        #     )
        #     cookies = self.browser.get_cookies()
        #     return cookies
        # except TimeoutException:
        #     return False



if __name__ == "__main__":
    from utils import CookiePool
    zh = Zhihu('1','1')
    zh.login()
