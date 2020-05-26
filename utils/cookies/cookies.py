#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/20 Wed
# TIME: 16:13:29
# DESCRIPTION:cookie相关api
import sqlite3
import os

def cookie2str(cookie_list):
    """
    cookie_list示例：[{sid: 'aaa'},{_qvc: 'bbb'}]
    cookie_list 转成字符串对象
    """
    cookie = ''
    for item in cookie_list:
        cookie = cookie + """{}={}; """.format(item['name'], item['value'])
    cookie = cookie.strip()
    return cookie


def cookie2dict(cookie_list):
    """
    cookie_list 转成字典对象
    """
    cookie = {}
    for item in cookie_list:
        for key, value in item.items():
            item[key] = str(value)
        cookie.update(item)
    return cookie


class CookiePool:
    """
    cookie池 数据库相关操作
    """
    __db = os.path.join(os.path.dirname(__file__), 'cookiePool.db')

    @classmethod
    def create_cookie_table(cls, table_name):
        conn = sqlite3.connect(cls.__db)
        cursor = conn.cursor()
        cursor.execute(
            'create table {}(id integer primary key AUTOINCREMENT ,cookie varchar(2000))'
            .format(table_name)
        )
        cursor.close()
        conn.commit()
        conn.close()

    @classmethod
    def drop_cookie_table(cls, table_name):
        conn = sqlite3.connect(cls.__db)
        cursor = conn.cursor()
        cursor.execute(
            'drop table {}'.format(table_name)
        )
        cursor.close()
        conn.commit()
        conn.close()

    @classmethod
    def insert_cookies(cls, table_name, cookies):
        """
        插入cookie
        cookies可以是 str 也可以是 list
        """
        if isinstance(cookies, str):
            cookies = [cookies]
        conn = sqlite3.connect(cls.__db)
        cursor = conn.cursor()
        for cookie in cookies:
            cursor.execute(
                'insert into {} (cookie) values ("{}")'
                .format(table_name, cookie))
        cursor.close()
        conn.commit()
        conn.close()

    @classmethod
    def delete_cookies(cls, table_name, ids):
        """
        删除cookie
        id可以是单个数字，也可以是列表
        id = None的时候删除所有
        """
        conn = sqlite3.connect(cls.__db)
        cursor = conn.cursor()

        if ids is None:
            cursor.execute('delete from {}'.format(table_name))
        else:
            if isinstance(ids, int):
                ids = '({})'.format(ids)
            elif isinstance(ids, list):
                ids = '({})'.format(str(ids)[1:-1])
            cursor.execute(
                'delete from {} where id in {}'
                .format(table_name, ids)
            )
        cursor.close()
        conn.commit()
        conn.close()

    @classmethod
    def get_cookies(cls, table_name):
        """
        获取cookie列表
        """
        conn = sqlite3.connect(cls.__db)
        cursor = conn.cursor()
        cursor.execute(
            'select id, cookie from {}'.format(table_name)
        )
        values = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        # return [{'id': _id, 'cookie': cookie} for (_id, cookie) in values]
        return values


if __name__ == "__main__":
    cp = CookiePool()
    print(cp.get_cookies('qcc'))
    # cp.delete_cookies('qcc', 1)