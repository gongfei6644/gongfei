# -*- coding: utf-8 -*-
# @Desc    : 导出标准化后有偏差的数据


import os
from datetime import datetime

from app.excel import ExcelExporter
from app.models.std_case import StdCase


class ExportDeviationData(ExcelExporter):
    def get_list(self, page_index):
        rt = StdCase().get_deviation_cases(page_index)
        return rt

    def assemble_row(self, sheet, case, row):
        self.set_cell(sheet, str(case.id), row, 1)
        self.set_cell(sheet, case.city_name, row, 2)
        self.set_cell(sheet, case.area_name, row, 3)
        self.set_cell(sheet, case.project_name, row, 4)
        self.set_cell(sheet, case.unitprice, row, 5)
        remark = case.std_remark
        if not remark and case.status == 0:
            remark = '重复案例'
        self.set_cell(sheet, remark, row, 6)


if __name__ == '__main__':
    row0 = ['ID', '城市', '区域', '楼盘', '单价', '备注']
    file = datetime.now().strftime('%Y%m%d') + '偏差案例数据.xlsx'
    file = os.path.join(os.path.dirname(__file__), file)

    exportor = ExportDeviationData()
    exportor.export(row0, file)
