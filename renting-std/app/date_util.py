# -*- coding: utf-8 -*-

from datetime import datetime


# 返回上个月的年月字符串
def get_last_month_ym(format='{}-{}'):
    now = datetime.now()
    y = now.year
    m = now.month
    if m == 1:
        m = 12
        y = y - 1
    else:
        m = m - 1
    lm = format.format(y, m)
    return lm


# 获取年月
def ym(date_str):
    date_str = date_str.strip()
    if len(date_str) > 10:
        date_str = date_str[0: 10]
    return date_str


if __name__ == '__main__':
    print(get_last_month_ym())
