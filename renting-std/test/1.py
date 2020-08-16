import os
from functools import reduce

import numpy as np
import pandas as pd

def get_list():
    df = pd.read_excel('宁波市_系数差_20191122134219.xlsx',sheet_name='楼层差修正系数')
    df_1 = pd.read_excel('宁波市_系数差_20191122134219.xlsx',sheet_name='朝向修正系数')
    df_2 = pd.read_excel('宁波市_系数差_20191122134219.xlsx',sheet_name='面积段修正系数')
    case = df.ix[:, ['*城市名称', '行政区', '楼盘名称', '*楼栋地上总层数','*所在楼层','*修正系数_百分比','*是否带电梯']].values
    case_1 = df_1.ix[:, ['*城市名称', '行政区', '楼盘名称', '*朝向','*修正系数_百分比']].values
    case_2 = df_2.ix[:, ['*城市名称', '行政区', '楼盘名称', '*建筑类型','*面积段','*修正系数_百分比']].values

    # print(case)
    # print('---',case_1)
    # print('****',case_2)

    # a = list(filter(lambda x:x[3]==2 and x[4] == 2,case))
    # b = list(filter(lambda x:x[3]=='西北',case_1))
    # c = list(filter(func,case_2))
    #
    # print(a,a[0])
    # print(b,b[0])
    # print(c,c[0])

    a = reduce(lambda x,y:x+y,case)[5]
    print(a)

def func(x):
    y = []
    if '~' in x[4]:
        a = x[4].split('~')
        a1 = a[0]
        a2 = a[1]
        print(a1,a2)
        x = np.append(x,[a1,a2])
        print('--***',x)
        y.append(x)
    else:
        y.append(x)
    print('--11--1',y)

    return y

get_list()



