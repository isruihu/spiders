#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/06/01 Mon
# TIME: 23:23:20
# DESCRIPTION:大众点评爬虫登录类
#             滑块拖动被识别了，暂未解决
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ROOT)

from utils.login import LoginBaseModule, get_tracks, move_to_gap
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


class Dzdianping(LoginBaseModule):
    def __init__(self, username, password):
        headless, imageless = False, False
        super(Dzdianping, self).__init__(headless=headless, imageless=imageless, user_agent=None)

        self.login_url = 'https://account.dianping.com/login?redir=http://www.dianping.com/'
        self.username = username
        self.password = password
        
    def login(self):
        self.browser.get(self.login_url)
        iframe = self.browser.find_element_by_xpath('//div[@class="mid-in"]/descendant::iframe')
        self.browser.switch_to.frame(iframe)
        print("switch to iframe")
        # 切换到账号登录
        time.sleep(2)
        self.browser_wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="bottom-password-login"]'))
        ).click()
        time.sleep(2)
        # 切换到密码登录
        self.browser_wait.until(
            EC.presence_of_element_located((By.XPATH, '//a[@id="tab-account"]'))
        ).click()
        time.sleep(2)
        # 输入手机号
        username_input = self.browser_wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="account-textbox"]'))
        )
        for _ in self.username:
            username_input.send_keys(_)
            time.sleep(0.1)
        # 输入密码
        password_input = self.browser_wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="password-textbox"]'))
        )
        for _ in self.password: 
            password_input.send_keys(_)
            time.sleep(0.1)

        self.browser.find_element_by_css_selector('button#login-button-account').click()
        time.sleep(2)

        tracks = get_tracks(230)
        try:
            slider = self.browser_wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="boxStatic "]'))
            )
            print(slider)
            move_to_gap(self.browser, slider, tracks)
        except TimeoutException:
            print("未找到滑块")
        time.sleep(5)
        cookies = self.browser.get_cookies()
        return cookies


if __name__ == "__main__":
    dzdp = Dzdianping('13675983285', '0.123456')
    dzdp.login()