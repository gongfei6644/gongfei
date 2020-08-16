# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 16:53
# @Author  : luomingming
# @Desc    :

import threading
import time

lock = threading.Lock()


def test():
    lock.acquire()
    for x in range(0, 10):
        print(x)
    lock.release()


t1 = threading.Thread(target=test)
t2 = threading.Thread(target=test)
t3 = threading.Thread(target=test)
t4 = threading.Thread(target=test)

t1.start()
t2.start()
t3.start()
t4.start()

