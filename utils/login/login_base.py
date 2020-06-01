#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/29 Fri
# TIME: 19:27:32
# DESCRIPTION:登录基础类
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(ROOT)
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from config import opt
from abc import abstractmethod, ABCMeta


class LoginBaseModule(metaclass=ABCMeta):
    cookie_table_name = None
    test_url = None

    def __init__(self, headless=True, imageless=True):

        options = Options()
         # 不加载图片，加快访问速度
        if imageless: 
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 设置为开发者模式，避免被识别
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        if headless:
            options.add_argument('--headless')
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

        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                cdc_adoQpoasnfa76pfcZLmcfl_Array = undefined
                cdc_adoQpoasnfa76pfcZLmcfl_Promise = undefined
                cdc_adoQpoasnfa76pfcZLmcfl_Symbol = undefined
            """
        })


    @abstractmethod
    def login(self):
        pass
