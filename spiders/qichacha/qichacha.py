#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/19 Tue
# TIME: 16:25:12
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ROOT)

from config import opt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import InvalidSelectorException, TimeoutException
import time
import numpy as np


class Qichacha:
    """
    企查查模拟登录
    """
    cookie_table_name = 'qcc'
    test_url = 'http://www.qcc.com/'

    def __init__(self, username, password):

        options = Options()
         # 不加载图片，加快访问速度
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 设置为开发者模式，避免被识别
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        
        self.browser = webdriver.Chrome(executable_path=opt.chrome_driver_path,
                                        options=options)
        self.browser_wait = WebDriverWait(self.browser, 20)
        # 设置浏览器窗口大小
        self.browser.set_window_size(1366,768)

        # 屏蔽 window.navigator.webdriver !!! 重要
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
        })

        self.login_url = 'https://www.qcc.com/user_login'

        self.username = username
        self.password = password

    def get_tracks(self, distance):
        """
        模拟人滑动滑块
        distance为传入的总距离
        """
        # 移动轨迹
        track=[]
        # 当前位移
        current=0
        # 减速阈值
        mid=distance*4/5
        # 计算间隔
        t=0.2
        # 初速度
        v=1

        while current<distance:
            if current<mid:
                # 加速度为2
                a=4
            else:
                # 加速度为-2
                a=-3
            v0=v
            # 当前速度
            v=v0+a*t
            # 移动距离
            move=v0*t+1/2*a*t*t
            # 当前位移
            current+=move
            # 加入轨迹
            track.append(round(move))
        return track
        
    def move_to_gap(self, slider, tracks):     # slider是要移动的滑块,tracks是要传入的移动轨迹
        driver = self.browser
        ActionChains(driver).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(driver).release().perform()

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
        tracks = self.get_tracks(distance=340)
        self.move_to_gap(slider=slider, tracks=tracks)
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
   pass