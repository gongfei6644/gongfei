# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 网站城市
class CityItem(scrapy.Item):
    # 城市名称
    city = scrapy.Field()
    # 区域
    area = scrapy.Field()
    # 片区
    sub_area = scrapy.Field()
    # 片区或区域（片区不存在时）链接
    sub_area_url = scrapy.Field()
    # 数据来源
    source = scrapy.Field()


# 案例
class CaseItem(scrapy.Item):
    # 唯一标识
    _id = scrapy.Field()
    # 城市名称
    city = scrapy.Field()
    # 区域
    area = scrapy.Field()
    # 片区
    sub_area = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 楼盘名称
    project_name = scrapy.Field()
    # 楼盘别名
    project_alias = scrapy.Field()
    # 户型结构
    house_structure = scrapy.Field()
    # 套内面积
    inside_space = scrapy.Field()
    # 使用面积
    usable_area = scrapy.Field()
    # 单价
    unitprice = scrapy.Field()
    # 总价
    total_price = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 户型
    house_type = scrapy.Field()
    # 建筑面积
    house_area = scrapy.Field()
    # 楼层
    floor_no = scrapy.Field()
    # 总楼层
    total_floor_num = scrapy.Field()
    # 朝向
    orientation = scrapy.Field()
    # 建筑年代
    build_date = scrapy.Field()
    # 案例类型
    case_type_code = scrapy.Field()
    # 装修
    decoration = scrapy.Field()
    # 有无电梯
    is_elevator = scrapy.Field()
    # 产权性质
    property_nature = scrapy.Field()
    # 房屋用途
    usage = scrapy.Field()
    # 建筑结构
    building_structure = scrapy.Field()
    # 案例时间
    case_happen_date = scrapy.Field()
    # 小区配套
    supporting_facilities = scrapy.Field()
    # 联系电话
    tel = scrapy.Field()
    # 是否已采集详情, 0: 表示访问正常，但页面没有数据或者响应状态为404；
    # 1: 表示正常；-1: 表示访问异常； 2：表示案例为一个月前的数据
    d_status = scrapy.Field()
    # 采集说明
    remark = scrapy.Field()
    # 详情采集时间
    detail_time = scrapy.Field()
    # 列表页地址
    list_page_url = scrapy.Field()
    # 数据源链接
    source_link = scrapy.Field()
    # 数据来源
    data_source = scrapy.Field()
    # 创建时间
    crt_time = scrapy.Field()


# 小区信息
class ProjectInfoItem(scrapy.Item):
    # 主键
    _id = scrapy.Field()
    # 小区信息唯一标识符
    uid = scrapy.Field()
    # 城市名称
    city = scrapy.Field()
    # 区域名称，即行政区
    area = scrapy.Field()
    # 片区
    sub_area = scrapy.Field()
    # 楼盘名称
    project_name = scrapy.Field()
    # 楼盘地址
    address = scrapy.Field()
    # 楼盘均价
    project_price = scrapy.Field()
    # 案例数量
    case_num = scrapy.Field()
    # 建筑用途
    usage = scrapy.Field()
    # 建筑年代
    build_date = scrapy.Field()
    # 评分
    grade = scrapy.Field()
    # 是否已采集详情, 0: 表示访问正常，但页面没有数据或者响应状态为404；
    # 1: 表示正常；-1: 表示访问异常； 2：表示案例为一个月前的数据
    d_status = scrapy.Field()
    # 采集说明
    remark = scrapy.Field()
    # 详情采集时间
    detail_time = scrapy.Field()
    # 列表页地址
    list_page_url = scrapy.Field()
    # 数据源链接
    source_link = scrapy.Field()
    # 数据来源
    data_source = scrapy.Field()
    # 创建时间
    crt_time = scrapy.Field()

