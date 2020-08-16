# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 16:48
# @Author  : luomingming
# @Desc    :


import json
from hashlib import md5


def uuid(lst):
    st = ''.join([str(v) for v in lst if v])
    md5_ = md5(st.encode('utf-8')).hexdigest()
    return md5_


def to_str(arg):
    if not arg:
        return None
    ret = ''
    if isinstance(arg, list) or isinstance(arg, tuple):
        ret = ''.join([str(i) for i in arg])
    elif isinstance(arg, dict):
        ret = json.dumps(arg, ensure_ascii=False)
    elif isinstance(arg, str):
        ret = arg
    return ret.strip()
