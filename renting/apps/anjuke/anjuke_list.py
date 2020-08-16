# coding=utf-8
import random
import re
import logging
import datetime
import time
import traceback
import requests
from lxml import etree
from urllib.parse import urljoin
from utils import common_tools
from utils.common_tools import get_rand_guid, get_full_url
from utils.unfont import Unfont


def list_anjuke(logger, content, sub_info):
    """"
    解析诸葛找房租房
    """
    logger.info("进入解析函数,{}".format(sub_info["page_url"]))
    data_list = []
    flag = "normal"
    if content == "404":
        flag = "finish"

    elif content == "retry":
        flag = "normal"
    else:
        html = etree.HTML(content)
        try:
            font_str = re.findall(r"charset=utf-8;base64,(.*?)'\)", content, re.S)
            unfont = Unfont(font_str[0]) if font_str else None
            items = html.xpath('//div[@id="list-content"]/div[@class="zu-itemmod"]')
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:
                now_time = datetime.datetime.now()  # 当前消息时间
                try:
                    title = item.xpath('.//h3//b/text()')[0].strip()  # 标题
                    title = unfont(title) if unfont else title
                    detail_href = item.xpath('.//h3/a/@href')[0].strip()
                    detail_url = get_full_url(sub_info["sub_area_url"], detail_href)
                    rent = item.xpath('.//div[@class="zu-side"]//p//text()')[0]  # 总价
                    rent = unfont(rent) if unfont else rent
                    unit = item.xpath('.//div[@class="zu-side"]/p//text()')
                    total_price = float(rent) * 10000 if "万" in unit else float(rent)
                    area = item.xpath('.//address[@class="details-item"]/text()[2]')[0].strip().split('-')[0]

                except:
                    pass  # 无效案例
                else:
                    try:
                        case_date = now_time.strftime("%Y%m")
                        guid = get_rand_guid(detail_url.split("?")[0], total_price, case_date)
                        dic_page = {"_id": guid,
                                    "data_source": sub_info["source"],
                                    "city": sub_info["city"],
                                    "title": title,
                                    "source_link": detail_url,
                                    "crt_time": now_time.strftime('%Y-%m-%d %H:%m:%S'),
                                    "total_price": total_price,
                                    # "area": sub_info["area"],
                                    "area": area,
                                    "sub_area": sub_info["sub_area"],
                                    "list_page_url": sub_info["page_url"],
                                    }
                    except:
                        logger.error(traceback.format_exc())
                    else:
                        data_list.append(dic_page)

            try:
                next_href = html.xpath('//a[contains(text(), "下一页")]')
                if not next_href or not data_list:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))

    dic_data = {"data": data_list, "flag": flag}
    print(dic_data)
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
