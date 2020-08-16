# -*- coding: utf-8 -*-



import traceback
import unittest

from app.config import EXPORT_FILE_DIR
from app.service.storage import *
from app.service.export_std import ExportStdCases


class StorageTestCase(unittest.TestCase):

    def test_copy_file(self):
        exporter = ExportStdCases(city='北京市', start_date='2019-05-01', end_date='2019-05-21')
        file = exporter.copy_file()
        print(file.replace(EXPORT_FILE_DIR, ''))

    def test_auto_in(self):
        start_date = '2018-02-10'
        end_date = '2018-03-10'
        exporter = ExportStdCases(city='北京市', start_date=start_date, end_date=end_date)
        exporter.export()

    def test_upload(self):
        try:
            upload(
                'D:\\workspace\\IDEAWorkspace\\git-projects\\daq-std\\exported_excel\\20190123174718自动入库201812月份案例数据.xlsx')
        except Exception as e:
            print(traceback.format_exc())
