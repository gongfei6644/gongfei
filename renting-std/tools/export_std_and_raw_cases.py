# -*- coding: utf-8 -*-
# @Desc    : 导出标准化及原始数据


import os
import time

from openpyxl import Workbook

from app.excel import ExcelExporter
from app.models.case import Case
from app.models.std_case import StdCase


class ExportStdAndRawCases(ExcelExporter):
    def __init__(self, city, start_date, end_date, std_date=None, data_source=None):
        self.wb = Workbook()
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.std_date = std_date
        self.data_source = data_source

    def get_list(self, page_index):
        rt = Case().get_std_cases(self.city, page_index, self.start_date, self.end_date,
                                  self.std_date, self.data_source)
        return rt

    def export(self, row0, file):
        sheet = self.wb.active
        for column in range(0, len(row0)):
            sheet.cell(row=1, column=column + 1).value = row0[column]
        page_index = 1
        row = 2
        while True:
            rt = self.get_list(page_index)
            if not rt:
                break
            ids = []
            for data in rt:
                ids.append(data.id)
            std_cases = StdCase().get_by_case_ids(ids, self.city)
            for data in rt:
                std_case = None
                for sc in std_cases:
                    if data.id == sc.case_id:
                        std_case = sc
                        break
                self.assemble_row(sheet, data, std_case, row)
                row = row + 1
            page_index = page_index + 1
        self.wb.save(file)

    def assemble_row(self, sheet, case, std_case, row):
        self.set_cell(sheet, case.city, row, 1)
        self.set_cell(sheet, case.project_name, row, 3)
        self.set_cell(sheet, case.area, row, 5)
        self.set_cell(sheet, case.build_name, row, 7)
        self.set_cell(sheet, case.floor_no, row, 9)
        self.set_cell(sheet, case.house_name, row, 11)
        self.set_cell(sheet, case.total_floor_num, row, 13)
        self.set_cell(sheet, case.case_happen_date, row, 15)
        self.set_cell(sheet, case.usage, row, 17)
        self.set_cell(sheet, case.build_area, row, 19)
        self.set_cell(sheet, case.unitprice, row, 21)
        self.set_cell(sheet, case.total_price, row, 23)
        self.set_cell(sheet, case.case_type, row, 25)
        self.set_cell(sheet, case.rental_method, row, 27)
        self.set_cell(sheet, case.deposit_method, row, 29)
        self.set_cell(sheet, case.orientation, row, 31)
        self.set_cell(sheet, case.build_type, row, 33)
        self.set_cell(sheet, case.house_type, row, 35)
        self.set_cell(sheet, case.house_structure, row, 37)
        self.set_cell(sheet, case.build_date, row, 39)
        self.set_cell(sheet, case.decoration, row, 41)
        self.set_cell(sheet, case.usable_area, row, 43)
        self.set_cell(sheet, case.remaining_years, row, 45)
        self.set_cell(sheet, case.new_ratio, row, 47)
        self.set_cell(sheet, case.currency, row, 49)
        self.set_cell(sheet, case.affiliated_house, row, 51)
        self.set_cell(sheet, case.supporting_facilities, row, 53)  # 配套
        self.set_cell(sheet, case.data_source, row, 55)
        self.set_cell(sheet, case.source_link, row, 57)
        self.set_cell(sheet, case.tel, row, 59)  # 来源电话
        self.set_cell(sheet, case.remark, row, 61)
        self.set_cell(sheet, case.is_std, row, 64)
        self.set_cell(sheet, case.std_remark, row, 65)

        if std_case:
            self.set_cell(sheet, std_case.city_name, row, 2)
            self.set_cell(sheet, std_case.project_name, row, 4)
            self.set_cell(sheet, std_case.area_name, row, 6)
            self.set_cell(sheet, std_case.build_name, row, 8)
            self.set_cell(sheet, std_case.floor_no, row, 10)
            self.set_cell(sheet, std_case.house_name, row, 12)
            self.set_cell(sheet, std_case.total_floor_num, row, 14)
            self.set_cell(sheet, std_case.case_happen_date, row, 16)
            self.set_cell(sheet, std_case.usage, row, 18)
            self.set_cell(sheet, std_case.build_area, row, 20)
            self.set_cell(sheet, std_case.unitprice, row, 22)
            self.set_cell(sheet, std_case.total_price, row, 24)
            self.set_cell(sheet, std_case.case_type, row, 26)
            self.set_cell(sheet, std_case.rental_method, row, 28)
            self.set_cell(sheet, std_case.deposit_method, row, 30)
            self.set_cell(sheet, std_case.orientation, row, 32)
            self.set_cell(sheet, std_case.build_type, row, 34)
            self.set_cell(sheet, std_case.house_type, row, 36)
            self.set_cell(sheet, std_case.house_structure, row, 38)
            self.set_cell(sheet, std_case.build_date, row, 40)
            self.set_cell(sheet, std_case.decoration, row, 42)
            self.set_cell(sheet, std_case.usable_area, row, 44)
            self.set_cell(sheet, std_case.remaining_years, row, 46)
            self.set_cell(sheet, std_case.new_ratio, row, 48)
            self.set_cell(sheet, std_case.currency, row, 50)
            self.set_cell(sheet, std_case.affiliated_house, row, 52)
            self.set_cell(sheet, std_case.supporting_facilities, row, 54)  # 配套
            self.set_cell(sheet, std_case.data_source, row, 56)
            self.set_cell(sheet, std_case.source_link, row, 58)
            self.set_cell(sheet, std_case.tel, row, 60)  # 来源电话
            self.set_cell(sheet, std_case.remark, row, 62)  # 备注
            self.set_cell(sheet, std_case.status, row, 63)
            #反调差标准差、反调差均差
            self.set_cell(sheet,std_case.adjust_std_price,row,66)
            self.set_cell(sheet,std_case.adjust_avg_price,row,67)


def export(city, start_date, end_date, std_date=None, data_source=None):
    file = city + start_date.replace('-', '') + '-' + end_date.replace('-', '') + '案例标准化及原始数据.xlsx'
    file = os.path.join(os.path.dirname(__file__), file)
    row0 = ['*城市名称', '标准化后', '*楼盘名称', '标准化后', '行政区', '标准化后', '楼栋名称', '标准化后',
            '所在楼层', '标准化后', '房号名称', '标准化后', '楼栋地上总层数', '标准化后', '*案例日期', '标准化后',
            '*案例用途', '标准化后', '*建筑面积', '标准化后', '*案例单价', '标准化后', '*案例总价', '标准化后',
            '*案例类型', '标准化后', '出租方式', '标准化后', '押付方式', '标准化后', '朝向', '标准化后', '建筑类型', '标准化后',
            '户型', '标准化后', '户型结构', '标准化后', '建筑年代', '标准化后', '装修', '标准化后', '使用面积', '标准化后',
            '剩余年限', '标准化后', '成新率', '标准化后', '币种', '标准化后', '附属房屋', '标准化后', '配套', '标准化后',
            '案例来源', '标准化后', '来源链接', '标准化后', '来源电话', '标准化后',"备注",'标准化后', '去重去偏差后的状态',
            '标准化状态', '标准化失败原因','反调差标准差','反调差均差']
    exportor = ExportStdAndRawCases(city=city, start_date=start_date, end_date=end_date,
                                    std_date=std_date, data_source=data_source)
    exportor.export(row0, file)


if __name__ == '__main__':
    cities = ["扬州市", "宿迁市", "无锡市", "淮安市", "苏州市", "泰州市", "南京市", "南通市", "徐州市",
                     "连云港市", "镇江市", "盐城市", "宜兴市", "常州市","郑州市","开封市","商丘市","许昌市","平顶山市"]
    # cities = ["南京市","郑州市"]
    data_source = None  # ['诸葛找房二手房', '房天下二手房', '城市房产二手房', '安居客二手房', '链家二手房', '赶集网二手房']
    start = '2017-01-01'
    end = '2019-11-31'
    std_date = None  # '2019-06-11 09:54:10'
    for city in cities:
        print("准备执行{}数据导出".format(city))
        t_start = time.time()
        export(city, start, end, std_date=std_date, data_source=data_source)
        t_end = time.time()
        print('{}数据导出完成, 耗时: {}秒'.format(city, t_end - t_start))
