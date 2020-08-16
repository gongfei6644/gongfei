# -*- coding: utf-8 -*-
# @Desc    :

from app.service.distinct import *
from app.switch_table import *

lst = cities()
mp = {}
for city in lst:
    city_name = city[1]
    idx = table_name_by_city('', city[1])
    if idx not in mp:
        mp[idx] = [city_name]
    else:
        tmp = mp[idx]
        tmp.append(city_name)
for k in mp.keys():
    print(k + '     ' + str(mp[k]))
