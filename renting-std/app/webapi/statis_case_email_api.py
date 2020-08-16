"""
采集、标准化数据统计邮件
"""

import datetime
import os
import time
import traceback
import requests
from flask import render_template, jsonify
from dateutil.relativedelta import relativedelta
from app.email import send

from app.webapi import api
from app.models.case import Case
from app.config import province_dict


def send_email():
    # 避免邮件发送两次 创建主进程时会发现此变量值为None，而创建子进程时此变量为true
    # if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    for i in range(10):
        try:
            url = 'http://127.0.0.1:8888/api/static/email' # nginx部署
            # url = 'http://127.0.0.1:5001/api/static/email'  # 测试
            res = requests.get(url)
            msg = res.text
            if msg:
                break
        except Exception as e:
            print(e)
            msg = '租金统计邮件程序出现异常: {}'.format(traceback.format_exc())
            send(msg, '租金统计邮件程序异常')
        time.sleep(0.5)
    while True:
        time.sleep(0.5)
        try:
            if datetime.datetime.now().strftime("%H:%M:%S") >= '08:00:00':
                print('发送邮件...')
                send(msg, '租金每日采集量统计报告--测试')
                print(msg)
                print('发送完成')
                break
        except Exception as e:
            print(e)
            msg = '租金统计邮件程序出现异常: {}'.format(traceback.format_exc())
            send(msg, '租金统计邮件程序异常')
            break


@api.route('/static/email', methods=['GET', 'POST'])
def static_email():
    dic = {}
    web_list = ['安居客租房', '城市房产租房', '房天下租房', '链家租房', '58同城租房']
    province_list = province_dict.keys()
    day_time = datetime.datetime.today().strftime("%Y-%m-%d")
    ls_day_time = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    mon_time = datetime.datetime.today().strftime("%Y-%m")
    ls_mon_time = (datetime.date.today() - relativedelta(months=1)).strftime("%Y-%m")
    year_time = datetime.datetime.today().strftime("%Y")
    week_time = int(time.localtime()[7] / 7 + 1) if datetime.datetime.today().weekday() != 0 else int(
        time.localtime()[7] / 7)
    week_day = time.localtime()[6]

    mond = datetime.datetime.today() - datetime.timedelta(days=week_day if week_day != 0 else 7)
    mond_time = mond.strftime('%Y-%m-%d')

    tuesd_time = (mond + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    wed_time = (mond + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    thurd_time = (mond + datetime.timedelta(days=3)).strftime('%Y-%m-%d')
    frid_time = (mond + datetime.timedelta(days=4)).strftime('%Y-%m-%d')
    satd_time = (mond + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    sund_time = (mond + datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    sund_next_time = (mond + datetime.timedelta(days=7)).strftime('%Y-%m-%d')

    get_static('case_count', dic, ls_day_time, day_time)
    get_static('std_count', dic, ls_day_time, day_time)
    get_static('proj_name_count', dic, ls_day_time, day_time)
    get_static('totalprice_count', dic, ls_day_time, day_time)

    if week_day >= 1 or week_day == 0:
        get_static('mond_count', dic, mond_time, tuesd_time)
        get_static('mond_std_count', dic, mond_time, tuesd_time)
    if week_day >= 2 or week_day == 0:
        get_static('tuesd_count', dic, tuesd_time, wed_time)
        get_static('tuesd_std_count', dic, tuesd_time, wed_time)
    if week_day >= 3 or week_day == 0:
        get_static('wed_count', dic, wed_time, thurd_time)
        get_static('wed_std_count', dic, wed_time, thurd_time)
    if week_day >= 4 or week_day == 0:
        get_static('thurd_count', dic, thurd_time, frid_time)
        get_static('thurd_std_count', dic, thurd_time, frid_time)
    if week_day >= 5 or week_day == 0:
        get_static('frid_count', dic, frid_time, satd_time)
        get_static('frid_std_count', dic, frid_time, satd_time)
    if week_day >= 6 or week_day == 0:
        get_static('satd_count', dic, satd_time, sund_time)
        get_static('satd_std_count', dic, satd_time, sund_time)
    if week_day == 0:
        get_static('sund_count', dic, sund_time, sund_next_time)
        get_static('sund_std_count', dic, sund_time, sund_next_time)

    get_static('mon_count', dic, mon_time, day_time)
    get_static('mon_std_count', dic, mon_time, day_time)
    get_static('mon_proj_name_count', dic, mon_time, day_time)
    get_static('mon_totalprice_count', dic, mon_time, day_time)

    get_static('ls_mon_count', dic, ls_mon_time, mon_time)
    get_static('ls_mon_std_count', dic, ls_mon_time, mon_time)
    get_static('ls_mon_proj_name_count', dic, ls_mon_time, mon_time)
    get_static('ls_mon_totalprice_count', dic, ls_mon_time, mon_time)

    get_static('province_count', dic, ls_day_time, day_time)

    get_all_static(dic, web_list)

    for key in dic.keys():
        if isinstance(dic[key], dict):
            for k, v in dic[key].items():
                if isinstance(v, int):
                    dic[key][k] = formatted_number(v)
        elif isinstance(dic[key], int):
            dic[key] = formatted_number(dic[key])

    # return jsonify(dic)
    return render_template("statics_email.html", params=locals())


def get_static(s_type, dic, ls_time, d_time):
    print('========', s_type, '=========')
    t = time.time()
    case = Case()
    result = case.statis(s_type, ls_time, d_time)

    if s_type != 'province_count':
        for i in result:
            dic[i['_id']['data_source']] = dic.get(i['_id']['data_source'], {})
            dic[i['_id']['data_source']][s_type] = dic[i['_id']['data_source']].get(s_type, 0)
            dic[i['_id']['data_source']][s_type] += i['count']
    else:
        for i in result:
            for pro, city_ls in province_dict.items():
                dic[i['_id']['data_source']][pro] = dic[i['_id']['data_source']].get(pro, 0)
                if i['_id']['city'] in city_ls:
                    dic[i['_id']['data_source']][pro] += i['count']
                    break
    print('用时：', time.time() - t, 's')


def get_all_static(dic, web_list):
    for web in web_list:
        dic['all_case_count'] = dic.get('all_case_count', 0)
        dic['all_case_count'] += dic[web].get('case_count', 0)

        dic['all_std_count'] = dic.get('all_std_count', 0)
        dic['all_std_count'] += dic[web].get('std_count', 0)

        dic['all_proj_name_count'] = dic.get('all_proj_name_count', 0)
        dic['all_proj_name_count'] += dic[web].get('proj_name_count', 0)

        dic['all_totalprice_count'] = dic.get('all_totalprice_count', 0)
        dic['all_totalprice_count'] += dic[web].get('totalprice_count', 0)

        dic['all_mond_count'] = dic.get('all_mond_count', 0)
        dic['all_mond_count'] += dic[web].get('mond_count', 0)
        dic['all_mond_std_count'] = dic.get('all_mond_std_count', 0)
        dic['all_mond_std_count'] += dic[web].get('mond_std_count', 0)

        dic['all_tuesd_count'] = dic.get('all_tuesd_count', 0)
        dic['all_tuesd_count'] += dic[web].get('tuesd_count', 0)
        dic['all_tuesd_std_count'] = dic.get('all_tuesd_std_count', 0)
        dic['all_tuesd_std_count'] += dic[web].get('tuesd_std_count', 0)

        dic['all_wed_count'] = dic.get('all_wed_count', 0)
        dic['all_wed_count'] += dic[web].get('wed_count', 0)
        dic['all_wed_std_count'] = dic.get('all_wed_std_count', 0)
        dic['all_wed_std_count'] += dic[web].get('wed_std_count', 0)

        dic['all_thurd_count'] = dic.get('all_thurd_count', 0)
        dic['all_thurd_count'] += dic[web].get('thurd_count', 0)
        dic['all_thurd_std_count'] = dic.get('all_thurd_std_count', 0)
        dic['all_thurd_std_count'] += dic[web].get('thurd_std_count', 0)

        dic['all_frid_count'] = dic.get('all_frid_count', 0)
        dic['all_frid_count'] += dic[web].get('frid_count', 0)
        dic['all_frid_std_count'] = dic.get('all_frid_std_count', 0)
        dic['all_frid_std_count'] += dic[web].get('frid_std_count', 0)

        dic['all_satd_count'] = dic.get('all_satd_count', 0)
        dic['all_satd_count'] += dic[web].get('satd_count', 0)
        dic['all_satd_std_count'] = dic.get('all_satd_std_count', 0)
        dic['all_satd_std_count'] += dic[web].get('satd_std_count', 0)

        dic['all_sund_count'] = dic.get('all_sund_count', 0)
        dic['all_sund_count'] += dic[web].get('sund_count', 0)
        dic['all_sund_std_count'] = dic.get('all_sund_std_count', 0)
        dic['all_sund_std_count'] += dic[web].get('sund_std_count', 0)

        dic[web]['week_count'] = dic[web].get('mond_count', 0) + dic[web].get('tuesd_count', 0) + \
                                 dic[web].get('wed_count', 0) + dic[web].get('thurd_count', 0) + \
                                 dic[web].get('frid_count', 0) + dic[web].get('satd_count', 0) + \
                                 dic[web].get('sund_count', 0)
        dic[web]['week_std_count'] = dic[web].get('mond_std_count', 0) + dic[web].get('tuesd_std_count', 0) + \
                                     dic[web].get('wed_std_count', 0) + dic[web].get('thurd_std_count', 0) + \
                                     dic[web].get('frid_std_count', 0) + dic[web].get('satd_std_count', 0) + \
                                     dic[web].get('sund_std_count', 0)

        dic['all_week_count'] = dic.get('all_week_count', 0)
        dic['all_week_count'] += dic[web]['week_count']
        dic['all_week_std_count'] = dic.get('all_week_std_count', 0)
        dic['all_week_std_count'] += dic[web]['week_std_count']

        dic['all_mon_count'] = dic.get('all_mon_count', 0)
        dic['all_mon_count'] += dic[web].get('mon_count', 0)

        dic['all_mon_std_count'] = dic.get('all_mon_std_count', 0)
        dic['all_mon_std_count'] += dic[web].get('mon_std_count', 0)

        dic['all_mon_proj_name_count'] = dic.get('all_mon_proj_name_count', 0)
        dic['all_mon_proj_name_count'] += dic[web].get('mon_proj_name_count', 0)

        dic['all_mon_totalprice_count'] = dic.get('all_mon_totalprice_count', 0)
        dic['all_mon_totalprice_count'] += dic[web].get('mon_totalprice_count', 0)

        dic['all_ls_mon_count'] = dic.get('all_ls_mon_count', 0)
        dic['all_ls_mon_count'] += dic[web].get('ls_mon_count', 0)

        dic['all_ls_mon_std_count'] = dic.get('all_ls_mon_std_count', 0)
        dic['all_ls_mon_std_count'] += dic[web].get('ls_mon_std_count', 0)

        dic['all_ls_mon_proj_name_count'] = dic.get('all_ls_mon_proj_name_count', 0)
        dic['all_ls_mon_proj_name_count'] += dic[web].get('ls_mon_proj_name_count', 0)

        dic['all_ls_mon_totalprice_count'] = dic.get('all_ls_mon_totalprice_count', 0)
        dic['all_ls_mon_totalprice_count'] += dic[web].get('ls_mon_totalprice_count', 0)

        dic[web]['std_rate'] = round((dic[web].get('std_count', 0) / dic[web]['case_count']) * 100, 1) \
            if dic[web].get('std_count', 0) and dic[web].get('case_count', 0) else 0
        dic[web]['mon_std_rate'] = round((dic[web].get('mon_std_count', 0) / dic[web]['mon_count']) * 100, 1) \
            if dic[web].get('mon_std_count', 0) and dic[web].get('mon_count', 0) else 0
        dic[web]['ls_mon_std_rate'] = round((dic[web].get('ls_mon_std_count', 0) / dic[web]['ls_mon_count']) * 100, 1) \
            if dic[web].get('ls_mon_std_count', 0) and dic[web].get('ls_mon_count', 0) else 0

    dic['all_std_rate'] = round((dic['all_std_count'] / dic['all_case_count']) * 100, 1) \
        if dic['all_std_count'] and dic['all_case_count'] else 0
    dic['all_mon_std_rate'] = round((dic['all_mon_std_count'] / dic['all_mon_count']) * 100, 1) \
        if dic['all_mon_std_count'] and dic['all_mon_count'] else 0
    dic['all_ls_mon_std_rate'] = round((dic['all_ls_mon_std_count'] / dic['all_ls_mon_count']) * 100, 1) \
        if dic['all_ls_mon_std_count'] and dic['all_ls_mon_count'] else 0


def formatted_number(num):
    if num > 1000:
        num_str = str(round(num / 10000, 1)) + 'w'
    else:
        num_str = num
    return num_str
