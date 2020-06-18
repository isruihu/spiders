#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/06/03 Wed
# TIME: 22:18:25
# DESCRIPTION:谷歌搜索 需要开代理
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(ROOT)

from utils.login import LoginBaseModule
from selenium.common.exceptions import TimeoutException
import time

class Google(LoginBaseModule):
    cookie_table_name = 'google'

    def __init__(self):
        super(Google, self).__init__(False, False)
        self.url = 'https://www.google.com.hk/search?&q=Microsoft'
        self.browser.set_page_load_timeout(15)

    def login(self):
        """谷歌搜索不用登录，所以直接返回cookie"""
        try:
            self.browser.get(self.url)
        except TimeoutException:
            raise RuntimeError("Can't visit {}".format(self.url))
        self.browser.save_screenshot(os.path.join(ROOT, 'images/{}.png'.format(time.time)))
        cookies = self.browser.get_cookies()
        return cookies


def google_cookie_check(cookie):
    pass


if __name__ == "__main__":
    from utils.cookies import CookiePool, cookie2str
    google = Google()
    cookie = google.login()
    CookiePool.insert_cookies(google.cookie_table_name, cookie2str(cookie))
    print(CookiePool.get_cookies(google.cookie_table_name))