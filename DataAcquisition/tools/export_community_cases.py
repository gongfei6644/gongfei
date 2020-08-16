# -*- coding: utf-8 -*-
# @Time    : 2019-06-10 13:46
# @Author  : luomingming
# @Desc    : 导出楼盘均价数据


import os
import time
from datetime import datetime

from FxtDataAcquisition.repository.project_info_repo import ProjectInfoRepo
from FxtDataAcquisition.utils.excel import ExcelExporter

pinfo_repo = ProjectInfoRepo()


class ExportCommunityCases(ExcelExporter):
    def __init__(self, city, start_date, end_date, data_source=None):
        ExcelExporter.__init__(self)
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.data_source = data_source

    def get_list(self, page_index):
        rt = pinfo_repo.find_all([self.city], self.start_date, self.end_date, self.data_source, page_index)
        return rt

    def assemble_row(self, sheet, case, row):
        self.set_cell(sheet, case.get('city'), row, 1)
        self.set_cell(sheet, case.get('area'), row, 2)
        self.set_cell(sheet, case.get('sub_area'), row, 3)
        self.set_cell(sheet, case.get('project_name'), row, 4)
        self.set_cell(sheet, case.get('address'), row, 5)
        self.set_cell(sheet, case.get('project_price'), row, 6)
        self.set_cell(sheet, case.get('case_num'), row, 7)
        self.set_cell(sheet, case.get('usage'), row, 8)
        self.set_cell(sheet, case.get('build_date'), row, 9)
        self.set_cell(sheet, case.get('grade'), row, 10)
        self.set_cell(sheet, case.get('list_page_url'), row, 11)
        self.set_cell(sheet, case.get('source_link'), row, 12)
        self.set_cell(sheet, case.get('data_source'), row, 13)


def export(city, start_date, end_date, data_source=None):
    file = city + start_date[0:10].replace('-', '') + '-' + end_date[0:10].replace('-', '') + '楼盘均价数据.xlsx'
    file = os.path.join(os.path.dirname(__file__), file)
    row0 = ['城市', '区域', '片区', '楼盘名称', '楼盘地址', '楼盘均价', '案例数量',
            '建筑用途', '建筑年代', '评分', '列表页地址', '数据源链接', '数据来源']
    exportor = ExportCommunityCases(city=city, start_date=start_date, end_date=end_date, data_source=data_source)
    exportor.export(row0, file)


if __name__ == '__main__':
    cities = ['南宁市']
    start_date = '2019-06-01 00:00:00'
    end_date = '2019-06-28 23:59:59'
    data_source = None
    for city in cities:
        print("准备执行{}数据导出".format(city))
        t_start = time.time()
        export(city, start_date, end_date, data_source=data_source)
        t_end = time.time()
        print('{}数据导出完成, 耗时: {}秒'.format(city, t_end - t_start))
