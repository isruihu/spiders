#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/20 Wed
# TIME: 16:28:08
# DESCRIPTION:将html写入文件中，便于查看
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(ROOT)


def write_html(html):
    with open(ROOT + '/res.html', 'w', encoding='utf-8') as f:
        f.write(html.text)