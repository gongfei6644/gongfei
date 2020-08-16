# -*- coding: utf-8 -*-
# @Desc    : 案例标准化


import logging
import os
import random
import re
import time
from datetime import datetime
from functools import reduce
import pandas as pd

import requests
from pymongo import UpdateOne

from app.config import CODE_TS
from app.models.case import Case
from app.models.std_case import StdCase
from app.service import distinct
from app.service import syscode
from app.service.unitprice_range import *

logger = logging.getLogger(__name__)

# -1表示中断标准化操作(因数据不合规范); 0表示操作正常
ERROR = -1
NORMAL = 0

# 北上广深城市ID
bsgs = {1, 2, 6, 7}
bs = {1, 2}

# 朝向类型
# orien_ts = ['东', '南', '西', '北', '东南', '东北', '西南', '西北', '南北', '东西']
orien_ts_m = {'南东': '东南', '北东': '东北', '南西': '西南', '北西': '西北', '北南': '南北', '西东': '东西'}

# 户型
house_ts = ['单房', '单身公寓', '一室一厅', '两室一厅', '两室两厅', '三室一厅', '三室两厅',
            '四室一厅', '四室两厅', '四室三厅', '五室', '六室', '七室及以上', '一室两厅',
            '两室零厅', '三室零厅', '四室四厅']

arabic_ch = {0: '零', 1: '一', 2: '两', 3: '三', 4: '四',
             5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
ch_arabic = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
             '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}

# 区域可能的后缀
area_suffixes = ['市城区', '市', '镇', '开发区', '高新区', '新区', '经济区', '经开区', '区', '自治县', '县']


def std():
    # cases = Case().find_page(0)
    # count = cases.count()
    # total_page = math.ceil(count / PAGE_SIZE)
    # logger.info('案例总数: {}, 总页数: {}, 查询数: {}'.format(count, total_page, cases.count(True)))
    #
    # for case in cases:
    #   logger.info(case.__dict__)
    num = 0
    t_start = time.time()
    while True:
        # 获取行政区非“周边”、“其他”的案例
        cases = Case().find()
        print(cases)
        # 如果没有数据可标准化则休眠30分钟
        if not cases:
            time.sleep(30)
            continue

        up_list = []
        ins_list = []
        city = cases[0].city
        for case in cases:
            print("正在标准化案例：", case.id, case.city, case.area, case.data_source, case.project_name, case.total_price)
            trim_case(case)
            # logger.info(case.__dict__) # __dict__不可输出数据了
            std_case = StdCase()
            std_case.case_id = case.id

            # 标准化行政区
            try:
                deal_district(case, std_case)
            except Exception as e:
                print("城市/行政区：", e)
                up_list.append(update_std_status(case, -1, "城市/行政区：" + str(e.args[0])))
                continue

            # 楼盘名处理
            project_name = case.project_name
            if not project_name:
                project_name = case.title
            if not project_name:
                logger.info("案例(id=[{}])的楼盘名不存在".format(case.id))
                up_list.append(update_std_status(case, -1, '楼盘名不存在'))
                continue
            try:
                project_name = deal_project_name(std_case, project_name, std_case.area_name, std_case.city_name,
                                                 std_case.city_id)
            except Exception as e:
                print("楼盘名称：", e)
                up_list.append(update_std_status(case, -1, "楼盘名称：" + str(e.args[0]) + '案列id:' + case.id))
                continue
            if filter_project(project_name) or filter_unsuitable(std_case.project_name):
                msg = "楼盘名不可为: 旁、旁边、对面、后面、附近、车库、商铺、厂房库房、店面、门面、写字楼、铺面"
                logger.info("[{}]案例(id=[{}])的{}".format(case.city, case.id, msg))
                up_list.append(update_std_status(case, -1, msg))
                continue
            std_case.project_name = project_name

            # 标准化案例时间
            try:
                deal_case_happen_date(case, std_case)
            except Exception as e:
                print("案例时间：", e)
                up_list.append(update_std_status(case, -1, "案例时间：" + str(e.args[0])))
                continue

            # 标准化案例时间
            if not case.case_happen_date:
                logger.info("[{}]案例(id=[{}])没有案例时间".format(case.city, case.id, case.case_happen_date))
                up_list.append(update_std_status(case, -1, '没有案例时间'))
                continue

            # 字段清洗：户型
            deal_house_type(case, std_case)
            # 字段清洗：户型结构
            deal_house_struct(case, std_case)
            # 字段清洗：装修
            deal_decoration(case, std_case)

            # 字段清洗：朝向、建筑年代、案例类型、币种、使用面积等
            deal_other_feilds(case, std_case)

            # 清洗字段：配套（使用原有数据）
            std_case.supporting_facilities = case.supporting_facilities

            source_link = case.source_link
            if source_link and len(source_link) > 200:
                source_link = ''
            std_case.source_link = source_link
            std_case.data_source = case.data_source
            std_case.tel = case.tel

            # 字段清洗：押付方式
            deal_deposit_method(case, std_case)

            # 字段清洗:楼栋地上总层数
            deal_total_floor(case, std_case)

            # 字段清洗: 所在楼层
            deal_floor_no(case, std_case)

            # 字段清洗：出租方式
            deal_rental_method(case, std_case)

            # 字段清洗：建筑面积
            try:
                deal_build_area(case, std_case)
            except Exception as e:
                print("建筑面积：", case.city, case.id, e)
                up_list.append(update_std_status(case, -1, "建筑面积：" + str(e.args[0])))
                logger.info("[{}]案例(id=[{}])建筑面积为空或者[{}]不匹配出租方式[{}]".format(case.city, case.id, case.build_area,
                                                                            case.rental_method))
                continue

            # 字段清洗：案例用途
            deal_usage(case, std_case)

            # 字段清洗：总价、单价
            try:
                deal_price(case, std_case)
            except Exception as e:
                print('总价/单价：', e)
                up_list.append(update_std_status(case, -1, '总价/单价：' + str(e.args[0])))
                logger.info(
                    "[{}]案例(id=[{}])总价或单价[{},{}]不匹配".format(case.city, case.id, case.total_price, case.unitprice))
                continue

            # 字段清洗:建筑类型

            deal_build_type(case, std_case)

            # 反调差字段：反调差标准价、反调差均价
            deal_adjust_price(std_case)

            # 保留空值字段
            std_case.build_name = None
            std_case.house_name = None
            std_case.usable_area = None
            std_case.new_ratio = None
            std_case.remaining_years = None
            std_case.affiliated_house = None
            std_case.remark = None

            ins_list.append(std_case.insert())
            up_list.append(update_std_status(case))

            num = num + 1
        # 保存标准化数据
        if ins_list:
            std_case.bulk_update(ins_list, city)
        # 标准化完成更新数据状态
        case.bulk_update(up_list, city)
        t_end = time.time()
        logger.info('标准化案例数: [{}], 耗时: [{}]秒'.format(num, t_end - t_start))


# 去空格
def trim_case(case):
    case.city = trim(case.city)
    case.area = trim(case.area)
    case.project_name = trim(case.project_name)
    case.build_date = trim(case.build_date)
    case.build_type = trim(case.build_type)
    case.house_type = trim(case.house_type)
    case.house_structure = trim(case.house_structure)
    case.floor_no = trim(case.floor_no)
    case.total_floor_num = trim(str(case.total_floor_num))
    case.usable_area = trim(case.usable_area)
    case.orientation = trim(case.orientation)
    case.unitprice = trim(str(case.unitprice))
    case.total_price = trim(str(case.total_price))
    case.usage = trim(case.usage)
    case.decoration = trim(case.decoration)
    case.supporting_facilities = trim(case.supporting_facilities)
    case.case_happen_date = trim(case.case_happen_date)
    case.source_link = trim(case.source_link)
    case.tel = trim(case.tel)
    case.data_source = trim(case.data_source)

    case.rental_method = trim(case.rental_method)
    case.build_area = trim(str(case.build_area))
    case.deposit_method = trim(case.deposit_method)
    case.case_type = trim(case.case_type)
    case.currency = trim(case.currency)

    case.sub_area = trim(case.sub_area)
    case.title = trim(case.title)
    case.address = trim(case.address)


def trim(val):
    if val:
        try:
            return re.sub(r'\s', '', val)
        except Exception as e:
            logger.error('去空格失败，原始数据: {}'.format(val))
            return val
    return None


# 过滤不合格的楼盘名
def filter_project(project_name):
    if project_name and (project_name.__contains__('旁') or project_name.__contains__('旁边')
                         or project_name.__contains__('对面') or project_name.__contains__('附近')
                         or project_name.__contains__('后面')):
        return True
    else:
        return False


# 过滤掉不合格的用途数据
def filter_unsuitable(usage):
    if usage and (usage.__contains__('车库') or usage.__contains__('商铺')
                  or usage.__contains__('厂房库房') or usage.__contains__('店面')
                  or usage.__contains__('门面') or usage.__contains__('写字楼')
                  or usage.__contains__('铺面')):
        return True
    else:
        return False


# 处理楼盘名
def deal_project_name(std_case, project_name, area='', city='', city_id=None):
    if not area:
        area = ''
    area_ = distinct.area_alias(city_id, area)
    city_ = distinct.city_alias(city)
    m = re.findall('[（(]+.+[)）]+', project_name)
    if m and ((area_ and m[0].__contains__(area_)) or (city_ and m[0].__contains__(city_))):
        idx = project_name.find('（')
        if idx == -1:
            idx = project_name.find('(')
        project_name = project_name[0:idx]
    else:
        exp = '（.*[路道号街巷弄栋旁]+.*|（别墅.*|（公寓.*|（商住楼.*|（备案名.*' \
              '|（.*旁边.*|（.*对面.*|（.*后面.*|（.*附近.*|（.*车库.*'
        m = re.findall(exp, project_name)
        if not m:
            m = re.findall(exp.replace('（', '\('), project_name)
        if m:
            project_name = project_name.replace(m[0], '')
            if '公寓' in m[0]:
                std_case.usage = '公寓'
            elif '商住楼' in m[0]:
                std_case.usage = '商住'

        m = re.findall('[1-9一二三四五六七八九十]{1,2}室.*', project_name)
        if m:
            project_name = project_name.replace(m[0], '')

    project_name = re.sub('\d+栋.*', '', project_name)
    project_name = re.sub('\d+单元.*', '', project_name)
    project_name = project_name.replace(city, '').replace(area, '')
    m = re.findall(r'[(（].*?\.\.\..*', project_name)
    if not m:
        m = re.findall(r'[(（].*?幢.*', project_name)
    if m:
        project_name = project_name.replace(m[0], '')
    project_name = project_name.replace('*', '')
    if '...' in project_name or '+' in project_name:
        msg = '[{}]的案例楼盘名称包含...或者+'.format(city)
        raise Exception(msg)
    return project_name


# 获取区域别名
def get_area_alias(area):
    return area[0: get_area_idx(area)]


def get_area_idx(area, idx=0):
    suffix = area_suffixes[idx]
    a = area.rfind(suffix)
    if a == -1 or (len(area) != (a + len(suffix))):
        idx = idx + 1
        if len(area_suffixes) == idx:
            return idx
        a = get_area_idx(area, idx)

    return a


# 标准化案例时间
def deal_case_happen_date(case, std_case):
    if case.case_happen_date:
        happen_date = str(case.case_happen_date)
        if '维护时间' in happen_date:
            happen_date = happen_date.replace('维护时间', '').replace('：', '')
        rt = re.match('^\d{2}[-]\d{2}', happen_date)
        if rt:
            yr = rt.group()
            now = datetime.now()
            nyr = str(now.year) + '-' + yr
            now_str = now.strftime('%Y-%m-%d')
            if nyr > now_str:
                nyr = str(now.year - 1) + '-' + yr
            std_case.case_happen_date = nyr
        else:
            dt = re.match('\d{4}[-]\d{2}[-]\d{2}', happen_date)
            if dt:
                std_case.case_happen_date = dt.group()
            else:
                try:
                    dt = re.match('\d{4}[-]\d+[-]\d+', happen_date).group()
                    splits = dt.split('-')
                    dt2 = splits[0] + '-'
                    if splits[1].__len__() == 1:
                        dt2 += '0' + splits[1] + '-'
                    else:
                        dt2 += splits[1] + '-'
                    if splits[2].__len__() == 1:
                        dt2 += '0' + splits[2]
                    else:
                        dt2 += splits[2]
                    std_case.case_happen_date = dt2
                except Exception as e:
                    raise Exception('[{}]案例(id=[{}])的案例时间有误[{}]'.format(case.city, case.id, case.case_happen_date))


# 处理行政区
def deal_district(case, std_case):
    city = distinct.city(case.city)
    if city:
        std_case.city(city)

        if case.area:
            area = None
            ca = '{}|{}'.format(case.city, case.area)
            dt = syscode.get_code(4)
            dt_v = None
            if dt and ca in dt.keys():
                dt_v = dt[ca]
            if dt_v:
                sp = dt_v.split(':')
                sp2 = sp[1].split('|')
                area = '{}:{}'.format(sp2[1], sp[0])
                std_case.city_name = sp2[0]
                std_case.city_id = None
            if not area:
                if std_case.city_name == '苏州市' and (case.area == '工业园' or case.area == '工业园区'):
                    area = distinct.area(std_case.city_id, '苏州工业园区')
                else:
                    area = distinct.area(std_case.city_id, case.area)
            if area:
                std_case.area(area)
            else:
                msg = "[{}]案例(id=[{}])的区域[{}]匹配不上".format(case.city, case.id, case.area)
                logger.info(msg)
                if case.area.__contains__('周边'):
                    raise Exception("[{}]案例(id=[{}])的区域[{}]不可为周边".format(case.city, case.id, case.area))
    else:
        msg = "[{}]案例(id=[{}])的城市[{}]匹配不上".format(case.city, case.id, case.city)
        logger.info(msg)
        raise Exception(msg)


def valid_floor_(case, num):
    if num:
        if num <= 3:
            area = float(re.findall(r'\d+\.?\d*', str(case.build_area))[0]) if case.build_area else 0
            if area >= 210:
                pass
            else:
                other_total_flo_ls = Case().find_total_floor(case.city, case.area, case.project_name)
                other_total_flo_ls = [int(a) for a in re.findall(r'\d+', str(other_total_flo_ls)) if a and int(a) >= 6]
                print('相同楼盘，其他楼栋总层数列表:', other_total_flo_ls)
                if len(other_total_flo_ls) == 0:
                    pass
                elif len(other_total_flo_ls) == 1:
                    num = other_total_flo_ls[0]
                elif len(other_total_flo_ls) > 1:
                    if max(other_total_flo_ls) - min(other_total_flo_ls) > 3:
                        num = None
                    else:
                        num = random.choice(other_total_flo_ls)
        else:
            pass
    else:
        num = None
    return num


def valid_floor(case, num):
    if num:
        if num <= 0:
            logger.info('所在楼层或总楼层为0')

        elif num > 60:
            msg = "[{}]案例(id=[{}])总楼层[{}]大于60，清空总楼层数据".format(case.city, case.id, num)
            logger.info(msg)
            return None
            # raise Exception(msg)
        else:
            return num
    return None


# 字段清洗：总楼层
def deal_total_floor(case, std_case):
    if case.total_floor_num:
        ret = re.findall("\\d+", case.total_floor_num)
        if ret:
            # num = valid_floor(case.id, std_case.city_id, int(ret[0]))
            num = valid_floor_(case, int(ret[0]))
            num = valid_floor(case, num) if num else None
        else:
            num = None
    else:
        num = None
    std_case.total_floor_num = num

    # 字段清洗：所在楼层


def deal_floor_no(case, std_case):
    floor = case.floor_no
    if floor and not floor.__contains__('共'):
        ret = re.findall("^\\d+$", floor)
        num = None
        if ret:
            num = int(ret[0])
        else:
            ret = re.findall("\\d+[层]", floor)
            if ret:
                num = int(str(ret[0]).rstrip('层'))

        t_num = std_case.total_floor_num
        if not num and t_num:
            t = t_num / 3
            if t < 1:
                num = random.randint(1, t_num)
            else:
                t = round(t)
                low = t
                medium = 2 * t
                high = t_num
                if floor.startswith('低'):
                    num = random.randint(1, low)
                elif floor.startswith('中'):
                    num = random.randint(low + 1, medium)
                elif floor.startswith('高'):
                    num = random.randint(medium + 1, high)
                elif floor == '顶层':
                    num = std_case.total_floor_num
        if num:
            std_case.floor_no = num
            if std_case.total_floor_num and num > std_case.total_floor_num:
                std_case.total_floor_num = None
            if std_case.floor_no > 60:
                std_case.floor_no = None


# 验证面积
def valid_area(house_area, case_id, city_id):
    if house_area > 1500:
        msg = "案例(id=[{}])面积[{}]不得大于1500平米".format(case_id, house_area)
        logger.info(msg)
        raise Exception(msg)
    elif bs.__contains__(int(city_id)) and house_area < 5:
        msg = "北京上海的案例(id=[{}])面积[{}]不得小于5平米".format(case_id, house_area)
        logger.info(msg)
        raise Exception(msg)
    elif not bs.__contains__(int(city_id)) and house_area < 15:
        msg = "非北京上海的案例(id=[{}])面积[{}]不得小于15平米".format(case_id, house_area)
        logger.info(msg)
        raise Exception(msg)


# 字段清洗：总价、单价
def deal_price(case, std_case):
    if case.total_price:
        r = re.findall(r'\d+\.?\d*', str(case.total_price))
        if r:
            if '百元' in str(case.total_price):
                t_pri = float(r[0]) * 100
            elif '千元' in str(case.total_price):
                t_pri = float(r[0]) * 1000
            elif '万元' in str(case.total_price):
                t_pri = float(r[0]) * 10000
            else:
                t_pri = float(r[0])
        else:
            t_pri = None
    else:
        t_pri = None
    std_case.total_price = t_pri
    try:
        unitprice = round(std_case.total_price / std_case.build_area, 2)
    except Exception as e:
        msg = "[{}]案例(id=[{}])单价为空，原因为：总价或建筑面积异常".format(case.city, case.id)
        logger.info(msg)
        raise Exception(msg)
    if unitprice < 2 or unitprice > 200:
        msg = "[{}]案例(id=[{}])单价[{}]不得小于2或大于200".format(case.city, case.id, unitprice)
        logger.info(msg)
        raise Exception(msg)
    std_case.unitprice = unitprice


# 字段清洗：建筑面积
def deal_build_area(case, std_case):
    if case.build_area:
        build_area = re.findall(r'\d+\.?\d*', str(case.build_area))[0]
        if not std_case.rental_method or std_case.rental_method == "整租":
            if float(build_area) >= 10 and float(build_area) <= 1500:
                area = float(build_area)
            else:
                msg = "出租方式为整租或为空的[{}]案例(id=[{}])建筑面积[{}]不得小于10平米不得大于1500平米".format(case.city, case.id, case.build_area)
                raise Exception(msg)
        elif std_case.rental_method == "合租":
            if float(build_area) >= 8 and float(build_area) <= 60:
                area = float(build_area)
            else:
                msg = "出租方式为合租的[{}]案例(id=[{}])建筑面积[{}]不得小于8平米不得大于60平米".format(case.city, case.id, case.build_area)
                raise Exception(msg)
        else:
            area = float(build_area)
    else:
        msg = "[{}]案例(id=[{}])建筑面积为空{}".format(case.city, case.id, case.build_area)
        raise Exception(msg)

    std_case.build_area = area


# 字段清洗：押付方式
def deal_deposit_method(case, std_case):
    # std_case.deposit_method = case.deposit_method
    if not case.deposit_method:
        if case.total_price:
            mtd = re.findall(r'[(（](.*?)[）)]', str(case.total_price))
            if mtd:
                mtd = mtd[0].strip()
            else:
                msg = '[{}],案例(id=[{}])押付方式为空'.format(case.city, case.id)
                logger.info(msg)
                return None
        else:
            return None
    else:
        mtd = case.deposit_method
    d_list = ['半年付', '年付', '季付', '月付', '面议']
    dep_mtd = [d for d in d_list if d in mtd]
    if dep_mtd and dep_mtd.__len__() >= 2:
        dep_method = '半年付'
    elif dep_mtd:
        dep_method = dep_mtd[0]
    else:
        try:
            ya = re.findall(r'押(.)', mtd)[0]
            fu = re.findall(r'付(.)', mtd)[0]
            ya_str = ya if ya in ch_arabic.keys() else arabic_ch[int(ya)]
            fu_num = ch_arabic[fu] if fu in ch_arabic.keys() else int(fu)
            fu_str = '三' if fu_num >= 3 else arabic_ch[fu_num]
            ya_str = "二" if ya_str == "两" else ya_str
            fu_str = "二" if fu_str == "两" else fu_str
            dep_method = "押" + ya_str + "付" + fu_str
        except Exception as e:
            dep_method = None
            msg = "[{}]案例(id=[{}])押付方式{}不匹配".format(case.city, case.id, case.deposit_method)
            logger.info(msg)
    std_case.deposit_method = dep_method


# 字段清洗：出租方式
def deal_rental_method(case, std_case):
    if case.rental_method:
        if '整租' in case.rental_method and '合租' in case.rental_method:
            rental_method = '可整租可合租'
        elif '整租' in case.rental_method:
            rental_method = '整租'
        elif '合租' in case.rental_method:
            rental_method = '合租'
        else:
            rental_method = None
    else:
        rental_method = None

    std_case.rental_method = rental_method


# 字段清洗：户型
def deal_house_type(case, std_case):
    ht = case.house_type
    if ht:
        # 将中文数字换成阿拉伯数字
        for w in ht:
            if w in ch_arabic.keys():
                ht = ht.replace(w, str(ch_arabic[w]))
        ht = ht.replace('房', '室')
        shi_1st = re.findall('\d+室', ht)
        ting_1st = re.findall('\d+厅', ht)
        wei = re.findall('\d+卫', ht)
        if shi_1st:
            shi = shi_1st[0]
            s = int(shi.replace('室', ''))
            if ting_1st:
                ting = ting_1st[0]
                ht = shi + ting
                t = int(ting.replace('厅', ''))
                if s > 4:
                    ht = shi
                    if s > 6:
                        ht = '七室及以上'
                else:
                    if (s == 1 and t > 2) or (s == 2 and t > 2) or (s == 3 and t > 2):
                        ht = shi + '2厅'
                    elif s == 4 and t > 4:
                        ht = shi + '4厅'
            elif s > 6:
                ht = '七室及以上'
        if (ht == '1室') or (ht == '2室') or (ht == '3室') or (ht == '4室'):
            return
        # 将阿拉伯数字换成中文
        for w in ht:
            try:
                if int(w) in arabic_ch.keys():
                    ht = ht.replace(w, arabic_ch[int(w)])
            except Exception as e:
                pass
        if ht == '一室' or ht == '一室零厅':
            if wei:
                ht = '单房'
            else:
                ht = '单身公寓'
        elif ht == '两室' or ht == '三室':
            ht = ht + '零厅'
        # elif ht == '四室' or ht == '四室零厅':
        #   ht = '四室一厅'

        if house_ts.__contains__(ht):
            std_case.house_type = ht
        else:
            logger.info("案例(id=[{}])户型[{}]不匹配".format(case.id, case.house_type))


# 字段清洗：户型结构
def deal_house_struct(case, std_case):
    if case.house_structure:
        codes = syscode.get_code(CODE_TS['户型结构'])
        try:
            if case.house_structure in codes.keys():
                k = case.house_structure
                v = codes[case.house_structure]
                if v.find(':') != -1:
                    k = v[v.find(':') + 1:]
                std_case.house_structure = k
        except Exception as e:
            logger.info("案例(id=[{}])户型结构[{}]异常[{}]".format(case.id, case.house_structure, e))


# 字段清洗：装修
def deal_decoration(case, std_case):
    if case.decoration:
        codes = syscode.get_code(CODE_TS['装修档次'])
        try:
            if case.decoration in codes.keys():
                k = case.decoration
                v = codes[case.decoration]
                if v.find(':') != -1:
                    k = v[v.find(':') + 1:]
                std_case.decoration = k
        except Exception as e:
            logger.info("案例(id=[{}])装修[{}]异常[{}]".format(case.id, case.decoration, e))


# 建筑类型清洗
def deal_build_type(case, std_case):
    if std_case.total_floor_num:
        tf = std_case.total_floor_num
        if tf >= 1 and tf <= 3:
            bt = '低层'
        elif tf >= 4 and tf <= 7:
            bt = '多层'
        elif tf == 8:
            if case.supporting_facilities and "电梯" in case.supporting_facilities:
                bt = '小高层'
            else:
                bt = '多层'
        elif tf >= 9 and tf <= 12:
            bt = '小高层'
        elif tf >= 13:
            bt = '高层'
        else:
            bt = std_case.total_floor_num
    else:
        bt = None
    std_case.build_type = bt

    # ----------------以下注释--------------------------------------------------------------
    # # if not std_case.building_type and case.building_type:
    # #   codes = syscode.get_code(code_ts['建筑类型'])
    # #   try:
    # #     if codes[case.building_type]:
    # #       k = case.building_type
    # #       v = codes[case.building_type]
    # #       if v.find(':') != -1:
    # #         k = v[v.find(':') + 1:]
    # #       std_case.building_type = k
    # #   except Exception as e:
    # #     logger.info("案例(id=[{}])建筑类型[{}]异常[{}]".format(case.id, case.building_type, e))


# 用途清洗
def deal_usage(case, std_case):
    su = case.usage
    if std_case.rental_method == '整租':
        if std_case.usage == '公寓' or std_case.usage == '商住':
            su = std_case.usage
        else:
            ha = std_case.build_area
            tfn = std_case.total_floor_num
            if tfn and tfn < 4 and ha > 180:
                su = '别墅'
            elif ha > 144:
                su = '非普通住宅'
            else:
                su = '普通住宅'
    elif not std_case.rental_method or std_case.rental_method == '合租':
        if case.usage == '公寓':
            su = '公寓'
        elif std_case.usage == '公寓' or std_case.usage == '商住':
            su = std_case.usage
        else:
            su = '普通住宅'
    std_case.usage = su


# 字段清洗：朝向、建筑年代、案例类型、币种、使用面积等
def deal_other_feilds(case, std_case):
    std_case.case_type = '月平方米租报盘'
    std_case.currency = '人民币'

    if case.orientation:
        ori = re.sub(r'[^东南西北]', '', case.orientation)
        if ori and ori.__len__() < 3:
            if ori.__len__() == 2 and orien_ts_m.get(ori):
                ori = orien_ts_m.get(ori)
            std_case.orientation = ori
    # 建筑年代
    if case.build_date:
        mt = re.match('\d{4}', case.build_date)
        b_date = None
        if mt:
            b_date = mt.group()
        if b_date:
            cur_year = time.localtime(time.time())[0]
            if (int(b_date) >= 1980) and (int(b_date) <= cur_year):
                std_case.build_date = b_date

    if case.usable_area:
        try:
            usable_area = float(case.usable_area)
        except Exception as e:
            r = re.findall('(\d+(\.\d+)?)', case.usable_area)
            if r:
                usable_area = float(r[0][0])
            else:
                usable_area = None
        if usable_area:
            std_case.usable_area = "{:.2f}".format(float(usable_area))
        else:
            std_case.usable_area = None


# 反调差字段：反调差标准价、反调差均价
def deal_adjust_price(std_case):

    total_floor = std_case.total_floor_num
    floor_no = std_case.floor_no
    if total_floor and floor_no:
        is_elevator = '是' if total_floor > 7 else '否'
        res_list_f = get_list('floor_deviation',t_floor=total_floor)
        if res_list_f:
            floor_deviation = judge(res_list_f,floor_no=floor_no,is_e = is_elevator)
            print('1', floor_deviation)
        else:
            floor_deviation = 0
    else:
        floor_deviation = 0

    print('2',floor_deviation)
    orientation = std_case.orientation
    if orientation:
        res_list_o = get_list('orientation_deviation')
        if res_list_o.any():
            orientation_deviation = judge(res_list_o,ori=orientation)
        else:
            orientation_deviation = 0
    else:
        orientation_deviation = 0

    build_type = std_case.build_type
    build_area = std_case.build_area

    print(total_floor,floor_no,orientation,build_type,build_area)
    if build_type:
        res_list_b = get_list('build_area_deviation', build_type=build_type)
        if res_list_b:
            build_area_deviation = judge(res_list_b, build_area=build_area)
        else:
            build_area_deviation = 0
    else:
        build_area_deviation = 0

    if any([floor_deviation, orientation_deviation, build_area_deviation]):
        print('----',floor_deviation, orientation_deviation, build_area_deviation)
        if std_case.unitprice:
            devi=1 + float(floor_deviation) + float(orientation_deviation) + float(build_area_deviation)
            std_case.adjust_std_price = round(std_case.unitprice / devi,2) if devi else None
        else:
            std_case.adjust_std_price = None
    else:
        std_case.adjust_std_price = None

    if std_case.adjust_std_price:

        if total_floor:
            floor_deviation_list = get_list('floor_deviation', t_floor=total_floor)
            if floor_deviation_list:
                print(floor_deviation_list)
                floor_deviation_sum = reduce(lambda x, y: x + y, floor_deviation_list)[5]
                floor_deviation_avg = round(floor_deviation_sum / len(floor_deviation_list), 1)
            else:
                floor_deviation_avg = 0
        else:
            floor_deviation_avg = 0

        if orientation:
            orientation_deviation_list = get_list('orientation_deviation')
            if orientation_deviation_list.any():
                orientation_deviation_sum = reduce(lambda x, y: x + y, orientation_deviation_list)[4]
                orientation_deviation_avg = round(orientation_deviation_sum / len(orientation_deviation_list), 1)
            else:
                orientation_deviation_avg = 0
        else:
            orientation_deviation_avg = 0

        if build_type:
            build_area_deviation_list = get_list('build_area_deviation', build_type=build_type)
            if build_area_deviation_list:
                build_area_deviation_sum = reduce(lambda x, y: x + y, build_area_deviation_list)[5]
                build_area_deviation_avg = round(build_area_deviation_sum / len(build_area_deviation_list), 1)
            else:
                build_area_deviation_avg = 0
        else:
            build_area_deviation_avg = 0

        if any([floor_deviation_avg, orientation_deviation_avg, build_area_deviation_avg]):
            std_case.adjust_avg_price = round(std_case.adjust_std_price * (
                        1 + floor_deviation_avg + orientation_deviation_avg + build_area_deviation_avg),2)
        else:
            std_case.adjust_avg_price = None
    else:
        std_case.adjust_avg_price = None


# 测试
def get_list(type,t_floor='',build_type=''):
    if type == 'floor_deviation':
        df = pd.read_excel(os.path.join(os.path.abspath('.'),'app\service\宁波市_系数差_20191122134219.xlsx'),sheet_name='楼层差修正系数')
        case = df.ix[:, ['*城市名称', '行政区', '楼盘名称', '*楼栋地上总层数', '*所在楼层', '*修正系数_百分比', '*是否带电梯']].values
        result = list(filter(lambda x: x[3] == t_floor, case))

    elif type == 'orientation_deviation':
        df = pd.read_excel(os.path.join(os.path.abspath('.'),'app\service\宁波市_系数差_20191122134219.xlsx'),sheet_name='朝向修正系数')
        case = df.ix[:, ['*城市名称', '行政区', '楼盘名称', '*朝向', '*修正系数_百分比']].values
        result = case

    elif type == 'build_area_deviation':
        df = pd.read_excel(os.path.join(os.path.abspath('.'),'app\service\宁波市_系数差_20191122134219.xlsx'),sheet_name='面积段修正系数')
        case = df.ix[:, ['*城市名称', '行政区', '楼盘名称', '*建筑类型','*面积段','*修正系数_百分比']].values
        result = list(filter(lambda x: x[3] == build_type, case))

    return result


def judge(res_list, floor_no=0, is_e='', ori='', build_area=0):
    for i in res_list:
        if floor_no and is_e:
            if i[4] == floor_no and i[6] == is_e:
                return i[5]
        elif ori:
            if i[3] == ori:
                return i[4]
        elif build_area:
            if '~' in i[4]:
                res = i[4].split('~')
                min = float(res[0])
                max = float(res[1])
                if build_area>=min and build_area<=max:
                    return i[5]
            else:
                res = re.findall(r'大于(\d+)',i[4])
                if res:
                    if build_area > int(res[0]):
                        return i[5]
                else:
                    res = re.findall(r'小于(\d+)', i[4])
                    if res:
                        if build_area < int(res[0]):
                            return i[5]

    return 0


# 更新案例标准化状态
def update_std_status(case, status=1, std_remark=None):
    # ret = Case().update_std_status(case, status, std_remark)
    op = UpdateOne({'_id': case.id}, {'$set': {
        'is_std': status, 'std_remark': std_remark, 'std_date': datetime.now()
    }}, upsert=False)
    return op
    # logger.info('案例{}更新结果: {}'.format(case.id, ret))


# 至少least_num个值不为空
def is_nblank(list, least_num):
    num = 0
    for v in list:
        if v:
            num = num + 1
    if num < least_num:
        return False
    return True


def get_blank(list):
    for v in list:
        if not v:
            return v
    return None
