import os
import time
import traceback

import requests
from flask import Flask, render_template
from utils.common_mongo import MongoOption
import datetime
from dateutil.relativedelta import relativedelta
from flask_apscheduler import APScheduler
from utils.statistics_send_email import send


class Config(object):  # 创建配置，用类
    # 任务列表
    JOBS = [
        {  # 第一个任务
            'id': 'job1',
            'func': '__main__:send_email',
            'args': '',
            'trigger': 'cron',  # cron表示定时任务
            'hour': 0,
            'minute': 35,
            'second': 0
        },
        # {  # 第二个任务，每隔5S执行一次
        #     'id': 'job2',
        #     'func': '__main__:send_email', # 方法名
        #     'args': (1,2), # 入参
        #     'trigger': 'interval', # interval表示循环任务
        #     'seconds': 5,
        # }
    ]


def send_email():
    # 避免邮件发送两次 创建主进程时会发现此变量值为None，而创建子进程时此变量为true
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        for i in range(10):
            try:
                url = 'http://127.0.0.1:8888/static/email'
                headers = {"User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1", }
                res = requests.get(url, headers=headers)
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
                    send(msg, '租金每日采集量统计报告')
                    print(msg)
                    print('发送完成，退出程序')
                    os._exit(1)
            except Exception as e:
                print(e)
                msg = '租金统计邮件程序出现异常: {}'.format(traceback.format_exc())
                send(msg, '租金统计邮件程序异常')
                return send_email()


# 创建flask的实例
app = Flask(__name__, template_folder="./templates")
app.config.from_object(Config())  # 为实例化的flask引入配置

mongo_client = MongoOption()


def formatted_number(num):
    if num > 1000:
        num_str = str(round(num / 10000, 1)) + 'w'
    else:
        num_str = str(num)
    return num_str


@app.route('/static/email', methods=['GET', 'POST'])
def static_email():
    province_dict = {'北京市': ['北京市', ], '深圳市': ['深圳市', ], '上海市': ['上海市', ], '广州市': ['广州市', ], '天津市': ['天津市', ],
                     '重庆市': ['重庆市', ],
                     '广东省': ["珠海市", "肇庆市", "梅州市", "中山市", "云浮市", "佛山市", "韶关市", "揭阳市", "江门市", "湛江市", "东莞市", "河源市", "潮州市",
                             "惠州市", "汕头市", "汕尾市", "清远市", "阳江市", "茂名市", ],
                     '江苏省': ["扬州市", "宿迁市", "无锡市", "淮安市", "苏州市", "泰州市", "南京市", "南通市", "徐州市", "连云港市", "镇江市", "盐城市", "宜兴市",
                             "常州市", ],
                     '浙江省': ["嘉兴市", "宁波市", "台州市", "衢州市", "舟山市", "杭州市", "金华市", "绍兴市", "湖州市", "丽水市", "温州市", ],
                     '山东省': ["泰安市", "济南市", "菏泽市", "德州市", "威海市", "日照市", "枣庄市", "东营市", "烟台市", "临沂市", "莱芜市", "淄博市", "青岛市",
                             "济宁市", "潍坊市", "聊城市", "滨州市", ],
                     '河南省': ["平顶山市", "三门峡市", "漯河市", "信阳市", "鹤壁市", "开封市", "濮阳市", "商丘市", "济源市", "周口市", "安阳市", "南阳市",
                             "郑州市", "驻马店市", "许昌市", "洛阳市", "新乡市", "焦作市", ],
                     '四川省': ["甘孜藏族自治州", "内江市", "成都市", "乐山市", "雅安市", "泸州市", "达州市", "绵阳市", "自贡市", "广元市", "遂宁市", "德阳市",
                             "巴中市", "眉山市", "资阳市", "广安市", "攀枝花市", "南充市", "阿坝藏族羌族自治州", "凉山彝族自治州", "宜宾市", ],
                     '湖北省': ["黄冈市", "襄阳市", "神农架林区", "鄂州市", "恩施土家族苗族自治州", "咸宁市", "武汉市", "潜江市", "孝感市", "十堰市", "天门市",
                             "宜昌市", "仙桃市", "荆门市", "黄石市", "随州市", "荆州市", ],
                     '湖南省': ["怀化市", "衡阳市", "湘西土家族苗族自治州", "株洲市", "长沙市", "邵阳市", "益阳市", "张家界市", "常德市", "湘潭市", "娄底市", "岳阳市",
                             "永州市", "郴州市", ],
                     '福建省': ["三明市", "福州市", "龙岩市", "漳州市", "莆田市", "泉州市", "宁德市", "厦门市", "南平市", ],
                     '河北省': ["秦皇岛市", "承德市", "石家庄市", "沧州市", "张家口市", "邢台市", "廊坊市", "保定市", "衡水市", "唐山市", "邯郸市", ],
                     '安徽省': ["合肥市", "宿州市", "芜湖市", "蚌埠市", "淮南市", "淮北市", "六安市", "马鞍山市", "安庆市", "宣城市", "黄山市", "池州市", "滁州市",
                             "铜陵市", "阜阳市", "亳州市", ],
                     '辽宁省': ["营口市", "盘锦市", "沈阳市", "朝阳市", "抚顺市", "葫芦岛市", "大连市", "本溪市", "铁岭市", "锦州市", "阜新市", "辽阳市", "鞍山市",
                             "丹东市", ],
                     '陕西省': ["铜川市", "榆林市", "西安市", "商洛市", "延安市", "宝鸡市", "咸阳市", "渭南市", "安康市", "汉中市", ],
                     '江西省': ["九江市", "南昌市", "宜春市", "抚州市", "赣州市", "新余市", "吉安市", "上饶市", "景德镇市", "鹰潭市", "萍乡市", ],
                     '广西省': ["玉林市", "来宾市", "南宁市", "北海市", "百色市", "河池市", "梧州市", "贵港市", "钦州市", "贺州市", "柳州市", "崇左市", "桂林市",
                             "防城港市", ],
                     '云南省': ["德宏傣族景颇族自治州", "昭通市", "怒江傈僳族自治州", "曲靖市", "大理白族自治州", "玉溪市", "丽江市", "临沧市", "保山市", "楚雄彝族自治州",
                             "文山壮族苗族自治州", "红河哈尼族彝族自治州", "昆明市", "迪庆藏族自治州", "普洱市", "西双版纳傣族自治州", ],
                     '山西省': ["临汾市", "忻州市", "大同市", "晋中市", "朔州市", "太原市", "晋城市", "运城市", "吕梁市", "长治市", "阳泉市", ],
                     '黑龙江省': ["鹤岗市", "绥化市", "牡丹江市", "大兴安岭地区", "双鸭山市", "佳木斯市", "鸡西市", "大庆市", "齐齐哈尔市", "哈尔滨市", "黑河市",
                              "伊春市", "七台河市", ],
                     '吉林省': ["吉林市", "通化市", "白山市", "敦化市", "松原市", "白城市", "四平市", "长春市", "延边朝鲜族自治州", "辽源市", ],
                     '贵州省': ["贵阳市", "六盘水市", "黔西南布依族苗族自治州", "毕节市", "铜仁市", "黔南布依族苗族自治州", "安顺市", "遵义市", "黔东南苗族侗族自治州", ],
                     '甘肃省': ["嘉峪关市", "天水市", "临夏回族自治州", "甘南藏族自治州", "庆阳市", "兰州市", "酒泉市", "张掖市", "定西市", "平凉市", "金昌市",
                             "武威市", "白银市", "陇南市", "临夏市", "甘南市", ],
                     '海南省': ["五指山市", "昌江黎族自治县", "西沙群岛", "三亚市", "临高县", "陵水黎族自治县", "万宁市", "屯昌县", "西南中沙群岛办事处（县级）", "三沙市",
                             "海口市", "儋州市", "琼中黎族苗族自治县", "琼海市", "定安县", "乐东黎族自治县", "南沙群岛", "东方市", "白沙黎族自治县", "中沙群岛岛礁及海域",
                             "文昌市", "澄迈县", "保亭黎族苗族自治县", ],
                     '西藏省': ["林芝地区", "山南地区", "拉萨市", "日喀则市", "昌都地区", "那曲地区", "阿里地区", ],
                     '新疆省': ["博尔塔拉蒙古自治州", "五家渠市", "铁门关市", "乌鲁木齐市", "阿拉尔市", "和田地区", "伊犁哈萨克自治州", "北屯市", "塔城地区", "阿克苏地区",
                             "哈密地区", "吐鲁番地区", "克拉玛依市", "巴音郭楞蒙古自治州", "石河子市", "昌吉回族自治州", "图木舒克市", "喀什地区", "阿勒泰地区",
                             "克孜勒苏柯尔克孜自治州", ],
                     '青海省': ["海南藏族自治州", "玉树藏族自治州", "海东市", "黄南藏族自治州", "海北藏族自治州", "西宁市", "海西蒙古族藏族自治州", "果洛藏族自治州", ],
                     '宁夏省': ["固原市", "中卫市", "吴忠市", "银川市", "石嘴山市", ],
                     '内蒙古': ["乌海市", "包头市", "赤峰市", "兴安盟", "通辽市", "呼和浩特市", "锡林郭勒盟", "巴彦淖尔市", "鄂尔多斯市", "乌兰察布市", "阿拉善盟",
                             "呼伦贝尔市", ]}
    province_list = province_dict.keys()
    webs = []
    web_list = ['安居客租房', '城市房产租房', '房天下租房', '链家租房', '58同城租房']
    day_time = datetime.datetime.today().strftime("%Y-%m-%d")
    ls_day_time = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    mon_time = datetime.datetime.today().strftime("%Y-%m")
    ls_mon_time = (datetime.date.today() - relativedelta(months=1)).strftime("%Y-%m")

    year_time = datetime.datetime.today().strftime("%Y")
    week_time = int(time.localtime()[7] / 7 + 1) if datetime.datetime.today().weekday() != 0 else int(
        time.localtime()[7] / 7)
    # print(week_time)
    week_day = time.localtime()[6]
    # print(week_day)

    mond = datetime.datetime.today() - datetime.timedelta(days=week_day if week_day != 0 else 7)
    mond_time = mond.strftime('%Y-%m-%d')

    tuesd_time = (mond + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    wed_time = (mond + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    thurd_time = (mond + datetime.timedelta(days=3)).strftime('%Y-%m-%d')
    frid_time = (mond + datetime.timedelta(days=4)).strftime('%Y-%m-%d')
    satd_time = (mond + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    sund_time = (mond + datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    sund_next_time = (mond + datetime.timedelta(days=7)).strftime('%Y-%m-%d')

    all_count = 0
    all_std_count = 0
    std_rate_avg = 0
    all_pro_count = 0
    all_total_pri_count = 0

    all_mond_count = 0
    all_mond_std_count = 0
    all_tuesd_count = 0
    all_tuesd_std_count = 0
    all_wed_count = 0
    all_wed_std_count = 0
    all_thurd_count = 0
    all_thurd_std_count = 0
    all_frid_count = 0
    all_frid_std_count = 0
    all_satd_count = 0
    all_satd_std_count = 0
    all_sund_count = 0
    all_sund_std_count = 0
    all_week_count = 0
    all_week_std_count = 0

    all_mon_count = 0
    all_mon_std_count = 0
    mon_std_rate_avg = 0
    all_mon_pro_count = 0
    all_mon_total_pri_count = 0

    all_ls_mon_count = 0
    all_ls_mon_std_count = 0
    ls_mon_std_rate_avg = 0
    all_ls_mon_pro_count = 0
    all_ls_mon_total_pri_count = 0

    for web in web_list:
        print('--------------------', web, '----------------------')
        web_dic = {}
        web_dic['name'] = web
        for i in range(50):
            collection = 'renting_case_{}'.format(str(i) if i >= 10 else '0' + str(i))
            print('*******************', collection, '********************')
            t1 = time.time()
            web_dic['count'] = web_dic.get('count', 0)
            web_dic['count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                         '$and': [{'detail_time': {'$exists': True}},
                                                                  {'detail_time': {'$gt': ls_day_time}},
                                                                  {'detail_time': {'$lt': day_time}}]}, collection)
            t2 = time.time()
            print(t2 - t1, 'count:', web_dic['count'])
            web_dic['std_count'] = web_dic.get('std_count', 0)
            web_dic['std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                             '$and': [{'is_std': {'$exists': True}}, {'is_std': 1},
                                                                      {'detail_time': {'$exists': True}},
                                                                      {'detail_time': {'$gt': ls_day_time}},
                                                                      {'detail_time': {'$lt': day_time}}]}, collection)
            t3 = time.time()
            print(t3 - t2, 'std_count:', web_dic['std_count'])

            t4 = time.time()
            # print(t4 - t3, 'std_rate:', web_dic['std_rate'])
            web_dic['pro_count'] = web_dic.get('pro_count', 0)
            web_dic['pro_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                             '$and': [{'project_name': {'$exists': True}},
                                                                      {'project_name': {'$nin': ['']}},
                                                                      {'detail_time': {'$exists': True}},
                                                                      {'detail_time': {'$gt': ls_day_time}},
                                                                      {'detail_time': {'$lt': day_time}}]}, collection)
            t5 = time.time()
            print(t5 - t4, 'pro_count:', web_dic['pro_count'])
            t6 = time.time()
            web_dic['total_pri_count'] = web_dic.get('total_pri_count', 0)
            web_dic['total_pri_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                   '$and': [{'total_price': {'$exists': True}},
                                                                            {'total_price': {'$nin': ['']}},
                                                                            {'detail_time': {'$exists': True}},
                                                                            {'detail_time': {'$gt': ls_day_time}},
                                                                            {'detail_time': {'$lt': day_time}}]},
                                                                  collection)
            t7 = time.time()
            print(t7 - t6, 'total_pri_count:', web_dic['total_pri_count'])
            web_dic['mond_count'] = web_dic.get('mond_count', 0)
            web_dic['mond_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                              '$and': [{'detail_time': {'$exists': True}},
                                                                       {'detail_time': {'$gt': mond_time}},
                                                                       {'detail_time': {'$lt': tuesd_time}}]},
                                                             collection)
            t8 = time.time()
            print(t8 - t7, 'mond_count:', web_dic['mond_count'])
            web_dic['mond_std_count'] = web_dic.get('mond_std_count', 0)
            web_dic['mond_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                  '$and': [{'is_std': {'$exists': True}}, {'is_std': 1},
                                                                           {'detail_time': {'$exists': True}},
                                                                           {'detail_time': {'$gt': mond_time}},
                                                                           {'detail_time': {'$lt': tuesd_time}}]},
                                                                 collection)
            t9 = time.time()
            print(t9 - t8, 'mond_std_count:', web_dic['mond_std_count'])
            web_dic['tuesd_count'] = web_dic.get('tuesd_count', 0)
            web_dic['tuesd_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                               '$and': [{'detail_time': {'$exists': True}},
                                                                        {'detail_time': {'$gt': tuesd_time}},
                                                                        {'detail_time': {'$lt': wed_time}}]},
                                                              collection) if week_day != 1 else 0
            t10 = time.time()
            print(t10 - t9, 'tuesd_count:', web_dic['tuesd_count'])
            web_dic['tuesd_std_count'] = web_dic.get('tuesd_std_count', 0)
            web_dic['tuesd_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                   '$and': [{'is_std': {'$exists': True}},
                                                                            {'is_std': 1},
                                                                            {'detail_time': {'$exists': True}},
                                                                            {'detail_time': {'$gt': tuesd_time}},
                                                                            {'detail_time': {'$lt': wed_time}}]},
                                                                  collection) if week_day != 1 else 0
            t11 = time.time()
            print(t11 - t10, 'tuesd_std_count:', web_dic['tuesd_std_count'])
            web_dic['wed_count'] = web_dic.get('wed_count', 0)
            web_dic['wed_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                             '$and': [{'detail_time': {'$exists': True}},
                                                                      {'detail_time': {'$gt': wed_time}},
                                                                      {'detail_time': {'$lt': thurd_time}}]},
                                                            collection) if week_day != 2 else 0
            t12 = time.time()
            print(t12 - t11, 'wed_count:', web_dic['wed_count'])
            web_dic['wed_std_count'] = web_dic.get('wed_std_count', 0)
            web_dic['wed_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                 '$and': [{'is_std': {'$exists': True}}, {'is_std': 1},
                                                                          {'detail_time': {'$exists': True}},
                                                                          {'detail_time': {'$gt': wed_time}},
                                                                          {'detail_time': {'$lt': thurd_time}}]},
                                                                collection) if week_day != 2 else 0
            t13 = time.time()
            print(t13 - t12, 'wed_std_count:', web_dic['wed_std_count'])
            web_dic['thurd_count'] = web_dic.get('thurd_count', 0)
            web_dic['thurd_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                               '$and': [{'detail_time': {'$exists': True}},
                                                                        {'detail_time': {'$gt': thurd_time}},
                                                                        {'detail_time': {'$lt': frid_time}}]},
                                                              collection) if week_day != 3 else 0
            t14 = time.time()
            print(t14 - t13, 'thurd_count:', web_dic['thurd_count'])
            web_dic['thurd_std_count'] = web_dic.get('thurd_std_count', 0)
            web_dic['thurd_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                   '$and': [{'is_std': {'$exists': True}},
                                                                            {'is_std': 1},
                                                                            {'detail_time': {'$exists': True}},
                                                                            {'detail_time': {'$gt': thurd_time}},
                                                                            {'detail_time': {'$lt': frid_time}}]},
                                                                  collection) if week_day != 3 else 0
            t15 = time.time()
            print(t15 - t14, 'thurd_std_count:', web_dic['thurd_std_count'])
            web_dic['frid_count'] = web_dic.get('frid_count', 0)
            web_dic['frid_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                              '$and': [{'detail_time': {'$exists': True}},
                                                                       {'detail_time': {'$gt': frid_time}},
                                                                       {'detail_time': {'$lt': satd_time}}]},
                                                             collection) if week_day != 4 else 0
            t16 = time.time()
            print(t16 - t15, 'frid_count:', web_dic['frid_count'])
            web_dic['frid_std_count'] = web_dic.get('frid_std_count', 0)
            web_dic['frid_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                  '$and': [{'is_std': {'$exists': True}}, {'is_std': 1},
                                                                           {'detail_time': {'$exists': True}},
                                                                           {'detail_time': {'$gt': frid_time}},
                                                                           {'detail_time': {'$lt': satd_time}}]},
                                                                 collection) if week_day != 4 else 0
            t17 = time.time()
            print(t17 - t16, 'frid_std_count:', web_dic['frid_std_count'])
            web_dic['satd_count'] = web_dic.get('satd_count', 0)
            web_dic['satd_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                              '$and': [{'detail_time': {'$exists': True}},
                                                                       {'detail_time': {'$gt': satd_time}},
                                                                       {'detail_time': {'$lt': sund_time}}]},
                                                             collection) if week_day != 5 else 0
            t18 = time.time()
            print(t18 - t17, 'satd_count:', web_dic['satd_count'])
            web_dic['satd_std_count'] = web_dic.get('satd_std_count', 0)
            web_dic['satd_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                  '$and': [{'is_std': {'$exists': True}}, {'is_std': 1},
                                                                           {'detail_time': {'$exists': True}},
                                                                           {'detail_time': {'$gt': satd_time}},
                                                                           {'detail_time': {'$lt': sund_time}}]},
                                                                 collection) if week_day != 5 else 0
            t19 = time.time()
            print(t19 - t18, 'satd_std_count:', web_dic['satd_std_count'])
            web_dic['sund_count'] = web_dic.get('sund_count', 0)
            web_dic['sund_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                              '$and': [{'detail_time': {'$exists': True}},
                                                                       {'detail_time': {'$gt': sund_time}},
                                                                       {'detail_time': {'$lt': sund_next_time}}]},
                                                             collection) if week_day != 6 else 0
            t20 = time.time()
            print(t20 - t19, 'sund_count:', web_dic['sund_count'])
            web_dic['sund_std_count'] = web_dic.get('sund_std_count', 0)
            web_dic['sund_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                  '$and': [{'is_std': {'$exists': True}}, {'is_std': 1},
                                                                           {'detail_time': {'$exists': True}},
                                                                           {'detail_time': {'$gt': sund_time}},
                                                                           {'detail_time': {'$lt': sund_next_time}}]},
                                                                 collection) if week_day != 6 else 0
            t21 = time.time()
            print(t21 - t20, 'sund_std_count:', web_dic['sund_std_count'])
            web_dic['week_count'] = web_dic.get('week_count', 0)
            web_dic['week_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                              '$and': [{'detail_time': {'$exists': True}},
                                                                       {'detail_time': {'$gt': mond_time}},
                                                                       {'detail_time': {'$lt': day_time}}]},
                                                             collection)
            t22 = time.time()
            print(t22 - t21, 'week_count:', web_dic['week_count'])
            web_dic['week_std_count'] = web_dic.get('week_std_count', 0)
            web_dic['week_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                  '$and': [{'is_std': {'$exists': True}}, {'is_std': 1},
                                                                           {'detail_time': {'$exists': True}},
                                                                           {'detail_time': {'$gt': mond_time}},
                                                                           {'detail_time': {'$lt': day_time}}]},
                                                                 collection)
            t23 = time.time()
            print(t23 - t22, 'week_std_count:', web_dic['week_std_count'])
            web_dic['mon_count'] = web_dic.get('mon_count', 0)
            web_dic['mon_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                             '$and': [{'detail_time': {'$exists': True}},
                                                                      {'detail_time': {'$gt': mon_time}}]},
                                                            collection) if day_time.split('-')[2] != '01' else 0
            t24 = time.time()
            print(t24 - t23, 'mon_count:', web_dic['mon_count'])
            web_dic['mon_std_count'] = web_dic.get('mon_std_count', 0)
            web_dic['mon_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                 '$and': [{'is_std': {'$exists': True}}, {'is_std': 1},
                                                                          {'detail_time': {'$gt': mon_time}}]},
                                                                collection) if day_time.split('-')[2] != '01' else 0
            t25 = time.time()
            print(t25 - t24, 'mon_std_count:', web_dic['mon_std_count'])

            t26 = time.time()
            web_dic['mon_pro_count'] = web_dic.get('mon_pro_count', 0)
            web_dic['mon_pro_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                 '$and': [{'project_name': {'$exists': True}},
                                                                          {'project_name': {'$nin': ['']}},
                                                                          {'detail_time': {'$exists': True}},
                                                                          {'detail_time': {'$gt': mon_time}}]},
                                                                collection)
            t27 = time.time()
            print(t27 - t26, 'mon_pro_count:', web_dic['mon_pro_count'])
            t28 = time.time()
            web_dic['mon_total_pri_count'] = web_dic.get('mon_total_pri_count', 0)
            web_dic['mon_total_pri_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                       '$and': [{'total_price': {'$exists': True}},
                                                                                {'total_price': {'$nin': ['']}},
                                                                                {'detail_time': {'$exists': True}},
                                                                                {'detail_time': {'$gt': mon_time}}]},
                                                                      collection)
            t29 = time.time()
            print(t29 - t28, 'mon_total_pri_count:', web_dic['mon_total_pri_count'])
            web_dic['ls_mon_count'] = web_dic.get('ls_mon_count', 0)
            web_dic['ls_mon_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                '$and': [{'detail_time': {'$exists': True}},
                                                                         {'detail_time': {'$gt': ls_mon_time}},
                                                                         {'detail_time': {'$lt': mon_time}}]},
                                                               collection)
            t30 = time.time()
            print(t30 - t29, 'ls_mon_count:', web_dic['ls_mon_count'])
            web_dic['ls_mon_std_count'] = web_dic.get('ls_mon_std_count', 0)
            web_dic['ls_mon_std_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                    '$and': [{'is_std': {'$exists': True}},
                                                                             {'is_std': 1},
                                                                             {'detail_time': {'$gt': ls_mon_time}},
                                                                             {'detail_time': {'$lt': mon_time}}]},
                                                                   collection)
            t31 = time.time()
            print(t31 - t30, 'ls_mon_std_count:', web_dic['ls_mon_std_count'])

            t32 = time.time()
            web_dic['ls_mon_pro_count'] = web_dic.get('ls_mon_pro_count', 0)
            web_dic['ls_mon_pro_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                    '$and': [{'project_name': {'$exists': True}},
                                                                             {'project_name': {'$nin': ['']}},
                                                                             {'detail_time': {'$exists': True}},
                                                                             {'detail_time': {'$gt': ls_mon_time}},
                                                                             {'detail_time': {'$lt': mon_time}}]},
                                                                   collection)
            t33 = time.time()
            print(t33 - t32, 'ls_mon_pro_count:', web_dic['ls_mon_pro_count'])

            t34 = time.time()
            web_dic['ls_mon_total_pri_count'] = web_dic.get('ls_mon_total_pri_count', 0)
            web_dic['ls_mon_total_pri_count'] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                                          '$and': [{'total_price': {'$exists': True}},
                                                                                   {'total_price': {'$nin': ['']}},
                                                                                   {'detail_time': {'$exists': True}},
                                                                                   {'detail_time': {
                                                                                       '$gt': ls_mon_time}},
                                                                                   {'detail_time': {'$lt': mon_time}}]},
                                                                         collection)
            t35 = time.time()
            print(t35 - t34, 'ls_mon_total_pri_count:', web_dic['ls_mon_total_pri_count'])
            for province in province_list:
                t36 = time.time()
                web_dic[province] = web_dic.get(province, 0)
                web_dic[province] += mongo_client.statistics({'d_status': 1, 'data_source': web,
                                                              '$and': [{'detail_time': {'$exists': True}},
                                                                       {'detail_time': {'$gt': ls_day_time}},
                                                                       {'detail_time': {'$lt': day_time}},
                                                                       {'city': {'$in': province_dict.get(province)}}]},
                                                             collection)
                t37 = time.time()
                print(t37 - t36, province + ':', web_dic[province])

        web_dic['std_rate'] = round((web_dic['std_count'] / web_dic['count']) * 100, 1) if web_dic['std_count'] and \
                                                                                           web_dic['count'] else 0
        web_dic['mon_std_rate'] = round((web_dic['mon_std_count'] / web_dic['mon_count']) * 100, 1) if web_dic[
                                                                                                           'mon_std_count'] and \
                                                                                                       web_dic[
                                                                                                           'mon_count'] else 0
        web_dic['ls_mon_std_rate'] = round((web_dic['ls_mon_std_count'] / web_dic['ls_mon_count']) * 100, 1) if web_dic[
                                                                                                                    'ls_mon_std_count'] and \
                                                                                                                web_dic[
                                                                                                                    'ls_mon_count'] else 0
        webs.append(web_dic)
        all_count += web_dic['count']
        all_std_count += web_dic['std_count']
        all_pro_count += web_dic['pro_count']
        # all_unit_pri_count += web_dic['unit_pri_count']
        all_total_pri_count += web_dic['total_pri_count']

        all_mond_count += web_dic['mond_count']
        all_mond_std_count += web_dic['mond_std_count']
        all_tuesd_count += web_dic['tuesd_count']
        all_tuesd_std_count += web_dic['tuesd_std_count']
        all_wed_count += web_dic['wed_count']
        all_wed_std_count += web_dic['wed_std_count']
        all_thurd_count += web_dic['thurd_count']
        all_thurd_std_count += web_dic['thurd_std_count']
        all_frid_count += web_dic['frid_count']
        all_frid_std_count += web_dic['frid_std_count']
        all_satd_count += web_dic['satd_count']
        all_satd_std_count += web_dic['satd_std_count']
        all_sund_count += web_dic['sund_count']
        all_sund_std_count += web_dic['sund_std_count']
        all_week_count += web_dic['week_count']
        all_week_std_count += web_dic['week_std_count']

        all_mon_count += web_dic['mon_count']
        all_mon_std_count += web_dic['mon_std_count']
        all_mon_pro_count += web_dic['mon_pro_count']
        # all_mon_unit_pri_count += web_dic['mon_unit_pri_count']
        all_mon_total_pri_count += web_dic['mon_total_pri_count']

        all_ls_mon_count += web_dic['ls_mon_count']
        all_ls_mon_std_count += web_dic['ls_mon_std_count']
        all_ls_mon_pro_count += web_dic['ls_mon_pro_count']
        # all_ls_mon_unit_pri_count += web_dic['ls_mon_unit_pri_count']
        all_ls_mon_total_pri_count += web_dic['ls_mon_total_pri_count']

    std_rate_avg = round((all_std_count / all_count) * 100, 1) if all_std_count and all_count else 0
    mon_std_rate_avg = round((all_mon_std_count / all_mon_count) * 100, 1) if all_mon_std_count and all_mon_count else 0
    ls_mon_std_rate_avg = round(
        (all_ls_mon_std_count / all_ls_mon_count) * 100, 1) if all_ls_mon_std_count and all_ls_mon_count else 0

    all_count = formatted_number(all_count)
    all_std_count = formatted_number(all_std_count)
    all_pro_count = formatted_number(all_pro_count)

    all_total_pri_count = formatted_number(all_total_pri_count)
    all_mond_count = formatted_number(all_mond_count)
    all_mond_std_count = formatted_number(all_mond_std_count)
    all_tuesd_count = formatted_number(all_tuesd_count)
    all_tuesd_std_count = formatted_number(all_tuesd_std_count)
    all_wed_count = formatted_number(all_wed_count)
    all_wed_std_count = formatted_number(all_wed_std_count)
    all_thurd_count = formatted_number(all_thurd_count)
    all_thurd_std_count = formatted_number(all_thurd_std_count)
    all_frid_count = formatted_number(all_frid_count)
    all_frid_std_count = formatted_number(all_frid_std_count)
    all_satd_count = formatted_number(all_satd_count)
    all_satd_std_count = formatted_number(all_satd_std_count)
    all_sund_count = formatted_number(all_sund_count)
    all_sund_std_count = formatted_number(all_sund_std_count)
    all_week_count = formatted_number(all_week_count)
    all_week_std_count = formatted_number(all_week_std_count)

    all_mon_count = formatted_number(all_mon_count)
    all_mon_std_count = formatted_number(all_mon_std_count)
    all_mon_pro_count = formatted_number(all_mon_pro_count)
    all_mon_total_pri_count = formatted_number(all_mon_total_pri_count)

    all_ls_mon_count = formatted_number(all_ls_mon_count)
    all_ls_mon_std_count = formatted_number(all_ls_mon_std_count)
    all_ls_mon_pro_count = formatted_number(all_ls_mon_pro_count)
    all_ls_mon_total_pri_count = formatted_number(all_ls_mon_total_pri_count)

    for web in webs:
        for key, value in web.items():
            if isinstance(value, int) and 'rate' not in key:
                web[key] = formatted_number(value)
        print(web)

    return render_template("statics_email.html", params=locals())


if __name__ == "__main__":
    try:
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
        app.run(debug=True, host='0.0.0.0', port="8888")
    except Exception as e:
        print(e)
        msg = '租金统计邮件程序出现异常: {}'.format(traceback.format_exc())
        send(msg, '租金统计邮件程序异常')
