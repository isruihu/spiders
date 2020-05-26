#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: ryan hu
# DATE: 2020/05/19 Tue
# TIME: 20:01:53
# DESCRIPTION:
# import threading

# def run():
#     import time
#     time.sleep(4)
#     print("{} finish.".format(threading.current_thread().name))

# def main():
#     threadings = []
#     for _ in range(5):
#         t = threading.Thread(target=run)
#         threadings.append(t)
#     for t in threadings:
#         t.setDaemon(True)
#         t.start()
#     for t in threadings:
#         t.join()
#     print("{} finish.".format(threading.current_thread().name))

# if __name__ == "__main__":
#     from  threading import Thread
#     import time
    
#     with open('res.html', 'r', encoding='utf-8') as f:
#         a = f.readlines()
#         print(a)