# coding=utf-8


from lxml import etree
import re
import datetime

import traceback
from utils import common_tools

from utils.common_tools import get_full_url
from utils.unfont import Unfont


def list_58tongcheng(logger, content, sub_info):
    """"
    解析58租房
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
            items = html.xpath('//ul[@class="house-list"]/li')

        except Exception as e:
            logger.error("解析案例节点异常:{},{}".format(e, sub_info["page_url"]))
        else:
            for item in items:
                try:
                    title = item.xpath('.//h2/a/text()')[0].strip()  # 标题
                    title = unfont(title) if unfont is not None else title
                    detail_href = item.xpath('.//h2/a/@href')[0]  # 详情链接
                    detail_url = get_full_url(sub_info["page_url"], detail_href)
                    # rent = item.xpath('.//span[@class="price"]/text()')[0].strip()  # 租金
                    rent = item.xpath('.//div[@class="money"]/b/text() | .//span[@class="price"]/text()')[
                        0].strip()  # 租金
                    rent = unfont(rent) if unfont is not None else rent
                    unit = item.xpath('.//p[@class="mt5 alingC"]/text() | .//div[@class="money"]')[0]
                    rent_total = float(rent) * 10000 if "万" in unit else float(rent)
                except:
                    # 无效案例
                    logger.error("检查无效案例{}".format(sub_info["page_url"]))
                else:
                    try:
                        crt_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        guid = common_tools.get_rand_guid(detail_url, rent_total, crt_time[:7])
                        dic_page = {
                            "_id": guid,
                            "data_source": sub_info["source"],
                            "city": sub_info["city"],
                            "title": title,
                            "source_link": detail_url,
                            "crt_time": crt_time,
                            # "area": sub_info["area"],
                            "sub_area": sub_info["sub_area"],
                            "list_page_url": sub_info["page_url"],
                        }
                    except Exception as e:
                        logger.error("解析数据异常{}, {}".format(e, traceback.format_exc()))
                    else:
                        data_list.append(dic_page)
            try:
                next_href = html.xpath("string(//a[contains(text(),'下一页')]/@href)")
                if not next_href or not data_list:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))
    dic_data = {"data": data_list, "flag": flag}
    print(dic_data)
    return dic_data
