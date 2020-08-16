# -*- coding: utf-8 -*-
# @Time    : 2019-05-07 21:13
# @Author  : luomingming
# @Desc    :

import threading
from FxtDataAcquisition.scheduler import sched_persist_cases, sched_field_statis


def persist():
    sched_persist_cases.start()


def statis():
    sched_field_statis.start()


t1 = threading.Thread(target=persist)
t2 = threading.Thread(target=statis)

t1.start()
t2.start()
