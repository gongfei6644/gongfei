# coding=utf-8
from urllib.parse import urljoin
import re
import datetime

import traceback
from common import CommonFun

import urllib3

urllib3.disable_warnings()


def list_qfang(url, cityname, area, sub_area, source, logger, content, **params):
    '''
               解析页面列表
               :param url:
               :return:
               '''
    dic_data = {}
    data_list = []
    # CommonFun.log_info("析取url="+url)
    if url.strip() == "":
        return dic_data

    list_page_url = url.strip()  # 当前列表页
    try:

        collecttype = "list"  # 列表类型

        items = content.xpath("//div[@id='cycleListings']/ul/li[@class='clearfix']")

        # print("items",len(items))
        for item in items:
            # 添加列表默认字段
            crt_time = datetime.datetime.now()  # 当前消息时间
            str_crt_time = crt_time.strftime("%Y-%m-%d %H:%M:%S")

            house_structure = ""  # 户型（如：一室一厅，两室一厅，两室两厅）
            project_alias = ""  # 楼盘别名
            inside_space = ""  # 套内面积
            usable_area = ""  # 使用面积

            # 房屋信息
            house_type = ""  # 户型
            house_area = ""  # 面积
            floor_no = ""  # 楼层
            orientation = ""  # 朝向
            build_date = ""  # 建筑年代
            total_floor_num = ""  # 总楼层
            orientation_list = ['东', '南', '西', '北']

            # 标题
            title = item.xpath("./div[@class='show-detail ']/p[@class='house-title']/a/text()")[0]
            title = re.sub(re.compile(r'\s+'), "", title)
            t_url = ""  # 详情链接
            t_url = item.xpath("./div[@class='show-detail ']/p[@class='house-title']/a/@href")[0]
            t_url = urljoin(url, t_url)
            # print("title",title,"url",t_url)
            plot_name = ""  # 楼盘名称
            address = ""  # 楼盘地址
            plot_name = item.xpath(".//p[@class='house-address clearfix']/span[@class='whole-line']/a/text()")  # 楼盘名称
            plot_name = plot_name[-1]
            try:
                address = item.xpath(".//div[@class='show-detail ']/p[@class='house-traffic clearfix']/span[1]/text()")[
                    0]  # 楼盘地址

            except Exception as err:
                address = ""

            houseInfo_list = item.xpath(
                ".//p[@class='house-about clearfix']/span/text()")  # .replace("\r\n", "").replace(" ", "")
            # houseInfo_list = houseInfo_desc.split('|')

            if len(houseInfo_list) > 0:
                for houseinfo in houseInfo_list:
                    # print("title", title, "plot_name", plot_name,"houseinfo",houseinfo)
                    if "室" in houseinfo:
                        house_type = houseinfo  # 户型
                    # 朝向
                    for flag in orientation_list:
                        if flag in houseinfo:
                            orientation = houseinfo
                            break
                    if '层' in houseinfo:
                        floor_no = houseinfo  # 楼层 低层(共7层)
                        # 拆分楼层和总楼层
                        if len(floor_no) > 0:
                            p_floor = floor_no
                            floor_no = re.findall("([低中高]{1}层)", p_floor)
                            if floor_no:
                                floor_no = floor_no[0]
                            else:
                                floor_no = ''
                            total_floor_num = re.findall("(\d+)", p_floor)
                            if total_floor_num:
                                total_floor_num = total_floor_num[0]
                            else:
                                total_floor_num = ''

                    if '年建' in houseinfo:
                        build_date = re.findall("(\d+)年建", houseinfo)
                        if build_date:
                            build_date = build_date[0]
                        else:
                            build_date = ""
                    if '㎡' in houseinfo or '平米' in houseinfo:
                        house_area = re.findall('(\d+(\.\d+)?)', houseinfo)[0][0]  # 面积 120平米

            # 建面单价和总价
            str_u_price = ""
            str_t_price = ""

            str_u_price = item.xpath(".//div[@class='show-price']/p/text()")[0]  # 建面单价

            str_t_price = item.xpath(".//div[@class='show-price']/span[@class='sale-price']/text()")[0]  # 总价

            u_price = re.findall('(\d+)', str_u_price)[0]  # 单价
            t_price = re.findall('\d+', str_t_price)[0]  # 总价

            if "万" in str_u_price:
                u_price = float(u_price) * 10000

            # 获取随机guid
            case_date = crt_time.strftime("%Y%m")
            guid = CommonFun.get_rand_guid(t_url, u_price, case_date)  # id 用单价和链接+当前月份
            dic_page = {"_id": guid, "city": cityname, "title": title, "source_link": t_url, "data_source": source,
                        "crt_time": str_crt_time, "house_structure": house_structure,
                        "project_alias": project_alias, "inside_space": inside_space,
                        "usable_area": usable_area, "unitprice": u_price, "total_price": t_price,
                        "address": address, "project_name": plot_name,
                        "house_type": house_type, "house_area": house_area, "floor_no": floor_no,
                        "total_floor_num": total_floor_num, "orientation": orientation,
                        "build_date": build_date, "area": area, "sub_area": sub_area, "case_type_code": 3001001,
                        "list_page_url": list_page_url
                        }

            print(dic_page)

            data_list.append(dic_page)  # 将数据字典添加到列表

        is_complete = False  # 是否采集完
        next_url = ""
        next_page = content.xpath("//a[@class='turnpage_next']/@href")
        if next_page:
            next_url = urljoin(url, next_page[0])
            logger.info("下一页链接:" + next_url)
            # item.update({'片区链接': next_url})

        else:
            # 已采集完
            is_complete = True

        dic_data.update(
            {"data": data_list, "next_url": next_url, "is_complete": is_complete})  # "warn_data": dic_warn,
    except Exception as ex:
        tb = traceback.format_exc()
        msg = "错误页面：来源{};错误信息：{};traceback：{}".format(source, url, ex, tb)
        logger.error(msg)
        # # 异常发消息预警
        # SendRabbitmq_msg("total", self.collecttype, self.cityname, self.source)
        dic_data = {}

    return dic_data
