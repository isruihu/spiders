#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/19 Tue
# TIME: 16:45:19
# DESCRIPTION:
import os

class Config:
    
    chrome_driver_path = os.path.join(os.path.dirname(__file__), 
                                      'chromedriver.exe')
    ip_proxy_server = 'http://112.124.25.99:8086'
    use_proxy = False # 是否使用代理Ip

opt = Config()