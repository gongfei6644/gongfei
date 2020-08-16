# coding=utf-8

import re
import logging
import datetime
import traceback
import requests
from lxml import etree
from urllib.parse import urljoin
from utils import common_tools


def list_zhongyuandichan(logger, content, sub_info):
    """"
    解析诸葛找房二手房
    """
    logger.info("进入解析函数,{}".format(sub_info["page_url"]))
    data_list = []
    flag = "normal"
    if content == "404":
        flag = "finish"

    elif content == "retry":
        flag = "normal"
    else:
        try:
            nodata = content.xpath('//div[@class="displaynone"]')
            if nodata:
                raise ValueError
            items = content.xpath('//div[@class="house-item clearfix"]')
        except ValueError:
            flag = "finish"
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:
                dic = {}
                # 添加列表默认字段
                crt_time = datetime.datetime.now()  # 当前消息时间
                try:
                    title = item.xpath('./div[@class="item-info fl"]/h4/a/@title')[0].strip()  # 标题
                    detail_href = item.xpath('./div[@class="item-info fl"]/h4/a/@href')[0].strip()
                    detail_url = detail_href if detail_href.startswith("http") else urljoin(
                        sub_info["sub_area_url"], detail_href)
                    unit_price = item.xpath('.//p[@class="price-txt tc"]/text()')[0]  # 单价
                    unit_price = re.findall(r'\d+\.?\d*', unit_price)[0]
                except:
                    # 无效案例
                    pass

                else:
                    try:
                        info_list = item.xpath('.//p[@class="house-name"]//text()')
                        info = re.sub('\s', "", "".join(info_list))  # 富通*丽沙花都|3室2厅|101.41平
                    except:
                        house_area, project_name, house_type = "", "", ""
                    else:
                        try:
                            project_name = re.match(r'(.+?)\|', info)
                            project_name = project_name.group(1)
                        except:
                            project_name = ""
                        try:
                            house_area = re.findall(r'(\d+\.?\d*)平', info)[0]  # 建筑面积
                        except:
                            house_area = ""
                        try:
                            house_type = re.findall(r'\|(\d*室\d*厅)', info)[0]  # 户型
                        except:
                            house_type = ""

                        try:
                            floor_no, total_floor_no = item.xpath(
                                'string(.//p[@class="house-txt"][1]/span[1]/text())').split("/")
                            floor_no = floor_no.replace("楼", "").strip()
                            total_floor_num = total_floor_no.replace("层", "").strip()
                        except:
                            floor_no, total_floor_num = "", ""

                        try:
                            orientation = item.xpath('string(.//p[@class="house-txt"][1]/span[2]/text())').strip()  # 朝向
                        except:
                            orientation = ""

                        try:
                            decoration = item.xpath('string(.//p[@class="house-txt"][1]/span[3]/text())').strip()  # 装修
                        except:
                            decoration = ""
                        try:
                            build_date = item.xpath(
                                'string(.//p[@class="house-txt"][1]/span[4]/text())').strip()  # 建筑年代
                        except:
                            build_date = ""
                        try:
                            total_price = item.xpath('string(.//p[@class="price-nub cRed tc"]/span/text())')  # 总价
                        except:
                            total_price = ""
                        try:
                            area_list = item.xpath('.//p[@class="house-txt"][2]/text()')
                            address = area_list[-1].strip()
                        except:
                            address = ""

                        try:
                            case_date = crt_time.strftime("%Y%m")
                            dic["_id"] = common_tools.get_rand_guid(detail_url, unit_price, case_date)
                            dic["list_page_url"] = sub_info["page_url"]
                            dic["case_type_code"] = 3001001
                            dic["data_source"] = sub_info["source"]
                            dic["city"] = common_tools.check_cityname(sub_info["city"])  # 返回标准城市名称
                            dic["area"] = sub_info["area"]
                            dic["sub_area"] = sub_info["sub_area"]
                            dic["crt_time"] = crt_time.strftime("%Y-%m-%d %H:%M:%S")
                            dic["title"] = title
                            dic["source_link"] = detail_url
                            dic["unitprice"] = unit_price
                            dic["house_area"] = house_area
                            dic["unitprice"] = unit_price
                            dic["project_name"] = project_name  # 小区/楼盘
                            dic["total_price"] = total_price
                            dic["house_type"] = house_type
                            dic["floor_no"] = floor_no
                            dic["build_date"] = build_date
                            dic["orientation"] = orientation  # 朝向
                            dic["total_floor_num"] = total_floor_num
                            dic["decoration"] = decoration  # 装修
                            dic["address"] = address

                        except:
                            print(traceback.print_exc())
                        else:
                            data_list.append(dic)

            try:
                next_href = content.xpath('string(//a[text()=">"]/@href)')
                if not next_href or not data_list:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))

    dic_data = {"data": data_list, "flag": flag}
    return dic_data


if __name__ == '__main__':
    url = "http://xm.ershoufang.zhuge.com/wuyuanwan/"
    headers = {'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
               'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)',
               }
    resp = requests.get(
        url,
        headers=headers)
    content = etree.HTML(resp.content.decode("utf-8"))
    html_str = {"str": resp.content.decode("utf-8")}
    logger = logging.getLogger("")