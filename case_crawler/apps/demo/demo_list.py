# coding=utf-8

import re
import datetime
import traceback
from urllib.parse import urljoin
from utils import common_tools


def list_demo(logger, content, sub_info):
    """
    解析诸葛找房二手房
    :param logger: 日志管理器
    :param content: HTML对象
    :param sub_info: 片区信息
    :return: {"data": data_list, "flag": flag}, flag有2种状态: "finish" / "normal"
    """
    logger.info("进入解析函数,{}".format(sub_info["page_url"]))
    data_list = []
    flag = "normal"

    if content == "404":
        flag = "finish"
    elif content == "retry":
        flag = "normal"

    else:
        # todo 从这里开始解析逻辑
        try:
            items = content.xpath('//ul[@id="listTableBox"]/li')
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:
                dic = {}
                # 添加列表默认字段
                crt_time = datetime.datetime.now()
                case_date = crt_time.strftime("%Y%m")
                str_crt_time = crt_time.strftime("%Y-%m-%d %H:%M:%S")

                try:
                    title = item.xpath('.//div[@class="title"]/a/@title')[0]  # 标题
                    t_url = item.xpath('.//div[@class="title"]/a/@href')[0]  # 详情链接
                    detail_url = t_url if t_url.startswith("http") else urljoin(sub_info["sub_area_url"], t_url)
                    unit_price = item.xpath('string(.//strong/text())').strip()  # 单价
                    unit_price = re.findall(r'\d+\.?\d*', unit_price)[0]
                except:
                    # 无效案例
                    logger.error("解析必要字段失败{}, 检查是否存在无效案例{}".format(traceback.format_exc(), sub_info))

                else:
                    guid = common_tools.get_rand_guid(detail_url, unit_price, case_date)
                    try:
                        info_list = item.xpath('string(./span[@class="list-table-info-box"]/span[2]/text())')
                        info = re.sub('\s', "", "".join(info_list))  # 169m²|4室2厅|高楼层|2018年建|南北
                    except:
                        house_area, floor_no, house_type, build_date, orientation = "", "", "", "", ""
                    else:
                        try:
                            house_area = re.findall(r'(\d+\.?\d*)m²', info)[0]  # 建筑面积
                        except:
                            house_area = ""
                        try:
                            house_type = re.findall(r'\|(\d*室\d*厅)', info)[0]  # 户型
                        except:
                            house_type = ""
                        try:
                            floor_no = re.findall(r'\|([高中低]楼层)', info)[0].replace("楼", "")  # 楼层
                        except:
                            floor_no = ""
                        try:
                            build_date = re.findall(r'(\d+年建)', info)[0]  # 建筑年代
                        except:
                            build_date = ""
                        try:
                            orientation = re.findall(r'\|([东南西北]+)', info)[0]  # 朝向
                        except:
                            orientation = ""
                    try:
                        case_happen_date = item.xpath(
                            'string(./span[@class="list-table-info-box"]/span[4]/text())').strip()
                        r = re.findall(r'(\d+)年(\d+)月(\d+)日', case_happen_date, re.S)
                        rl = list(r[0])
                        rl[2] = rl[2] if len(rl[2]) > 1 else rl[2].rjust(2, "0")
                        rl[1] = rl[1] if len(rl[1]) > 1 else rl[1].rjust(2, "0")
                        case_happen_date = "-".join(rl)

                    except:
                        case_happen_date = ""

                    try:
                        total_price = item.xpath('string(.//b/text())')  # 总价
                    except:
                        total_price = ""
                    try:
                        area_list = item.xpath('.//span[@class="list-table-info-box"]/span[1]//text()')
                        area_str = re.sub('\s', "", "".join(area_list))  # [罗湖-东门-联城美园]罗湖深南东路与南极路交汇处
                    except:
                        project_name, address = "", ""
                    else:
                        try:
                            project_name = re.findall(
                                r'\[.*-(.+?)\].*$', area_str)[0] if "-" in area_str else re.findall(
                                r'\[(.*)\].*$', area_str)[0]
                        except:
                            project_name = ""
                        try:
                            address = re.findall(r'\](.*$)', area_str)[0]
                        except:
                            address = ""

                    try:
                        dic["case_type_code"] = 3001001
                        dic["data_source"] = sub_info["source"]
                        dic["city"] = sub_info["city"]
                        dic["crt_time"] = str_crt_time
                        dic["title"] = title
                        dic["source_link"] = detail_url
                        dic["unitprice"] = unit_price
                        dic["house_area"] = house_area
                        dic["unitprice"] = unit_price
                        dic["project_name"] = project_name  # 小区/楼盘
                        dic["case_happen_date"] = case_happen_date  # 案例时间
                        dic["total_price"] = total_price
                        dic["house_type"] = house_type
                        dic["floor_no"] = floor_no
                        dic["build_date"] = build_date
                        dic["orientation"] = orientation
                        dic["area"] = sub_info["area"]
                        dic["sub_area"] = sub_info["sub_area"]
                        dic["address"] = address

                        dic["_id"] = guid
                    except:
                        print(traceback.print_exc())
                    else:
                        data_list.append(dic)

            # todo 判断是否存在下一页
            try:
                next_href = content.xpath('//a[@class="laypage-next"]/@href')[0]
                if not next_href:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))

    dic_data = {"data": data_list, "flag": flag}
    return dic_data


if __name__ == '__main__':
    # url = "http://xm.ershoufang.zhuge.com/wuyuanwan/"
    # headers = {'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    #            'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)',
    #            }
    # resp = requests.get(
    #     url,
    #     headers=headers)
    # content = etree.HTML(resp.content.decode("utf-8"))
    # html_str = {"str": resp.content.decode("utf-8")}
    # logger = logging.getLogger("")
    list_demo("", "", "")
