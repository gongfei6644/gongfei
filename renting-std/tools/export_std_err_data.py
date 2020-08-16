# -*- coding: utf-8 -*-
# @Desc    : 导出标准化有问题的数据


import os
from datetime import datetime

from app.excel import ExcelExporter
from app.models.case import Case


class ExportStdErrData(ExcelExporter):
    def __init__(self, city, start_date, end_date):
        ExcelExporter.__init__(self)
        self.city = city
        self.start_date = start_date
        self.end_date = end_date

    def get_list(self, page_index):
        rt = Case().get_std_err_cases(self.city, page_index, self.start_date, self.end_date)
        return rt

    def assemble_row(self, sheet, case, row):
        self.set_cell(sheet, case.id, row, 1)
        self.set_cell(sheet, case.city, row, 2)
        self.set_cell(sheet, case.area, row, 3)
        self.set_cell(sheet, case.project_name, row, 4)
        self.set_cell(sheet, case.case_happen_date, row, 5)
        self.set_cell(sheet, case.usage, row, 6)
        self.set_cell(sheet, case.build_area, row, 7)
        self.set_cell(sheet, case.unitprice, row, 8)
        self.set_cell(sheet, case.total_price, row, 9)
        self.set_cell(sheet, case.build_type, row, 10)
        self.set_cell(sheet, case.std_remark, row, 11)


if __name__ == '__main__':
    city = '北京市'
    start_date = datetime.strptime('2019-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2019-02-25', '%Y-%m-%d')
    file = city + start_date.strftime('%Y%m%d') + '-' + end_date.strftime('%Y%m%d') + '案例标准化失败数据.xlsx'
    file = os.path.join(os.path.dirname(__file__), file)
    row0 = ['ID', '城市', '区域', '楼盘', '案例时间', '用途', '面积', '单价', '总价', '建筑类型', '标准化失败原因']
    exportor = ExportStdErrData(city=city, start_date=start_date, end_date=end_date)
    exportor.export(row0, file)
