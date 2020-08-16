# -*- coding: utf-8 -*-
# @Desc    : 导出标准化数据


import os
import time

from app.service.export_std import ExportStdCases


class ExportStdCase(ExportStdCases):

    def assemble_row(self, sheet, case, row):
        self.set_cell(sheet, case.city_name, row, 1)
        self.set_cell(sheet, case.project_name, row, 2)
        self.set_cell(sheet, case.area_name, row, 3)
        self.set_cell(sheet, '', row, 4)  # 楼栋名称
        self.set_cell(sheet, case.floor_no, row, 5)
        self.set_cell(sheet, '', row, 6)  # 房号名称
        self.set_cell(sheet, case.total_floor_num, row, 7)
        self.set_cell(sheet, case.case_happen_date, row, 8)
        self.set_cell(sheet, case.usage, row, 9)
        self.set_cell(sheet, case.house_area, row, 10)
        self.set_cell(sheet, case.unitprice, row, 11)
        self.set_cell(sheet, case.total_price, row, 12)
        self.set_cell(sheet, case.case_type, row, 13)
        self.set_cell(sheet, case.orientation, row, 14)
        self.set_cell(sheet, case.building_type, row, 15)
        self.set_cell(sheet, case.house_type, row, 16)
        self.set_cell(sheet, case.house_structure, row, 17)
        self.set_cell(sheet, case.build_date, row, 18)
        self.set_cell(sheet, case.decoration, row, 19)
        self.set_cell(sheet, case.usable_area, row, 20)
        self.set_cell(sheet, '', row, 21)  # 剩余年限
        self.set_cell(sheet, '', row, 22)  # 成新率
        self.set_cell(sheet, case.currency, row, 23)
        self.set_cell(sheet, '', row, 24)  # 附属房屋
        self.set_cell(sheet, case.supporting_facilities, row, 25)  # 配套
        self.set_cell(sheet, case.data_source, row, 26)
        self.set_cell(sheet, case.source_link, row, 27)
        self.set_cell(sheet, case.tel, row, 28)  # 来源电话
        self.set_cell(sheet, case.status, row, 29)  # 备注


def export(city, start_date, end_date):
    file = city + start_date.replace('-', '') + '-' + end_date.replace('-', '') + '标准化案例数据.xlsx'
    file = os.path.join(os.path.dirname(__file__), file)
    exportor = ExportStdCase(city=city, start_date=start_date, end_date=end_date, status=None, file=file)
    exportor.export()


if __name__ == '__main__':
    cities = ['嘉兴市']
    start = '2019-07-08'
    end = '2019-07-15'
    for city in cities:
        print("准备执行{}数据导出".format(city))
        t_start = time.time()
        export(city, start, end)
        t_end = time.time()
        print('{}数据导出完成, 耗时: {}秒'.format(city, t_end - t_start))
