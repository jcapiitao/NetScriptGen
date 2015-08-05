# -*-coding:UTF-8 -*

from unittest import TestCase
from utils.ExcelWorkbookManager import *
import xlrd


class ExcelWorkbookManagerTests(TestCase):

    test_file = 'test.xlsx'
    path = get_full_path(test_file)

    def test_get_test_excel_file(self):
        self.assertEqual(get_full_path() + '/' + self.test_file, self.path)

    def test_get_excel_workbook(self):
        self.assertIsInstance(get_excel_workbook(), type(xlrd.open_workbook(self.path)))

    def test_get_sheet(self):
        wb = xlrd.open_workbook(self.path)
        sheet = wb.sheet_by_name('interface_test')
        self.assertIsInstance(get_sheet('interface_test'), type(sheet))

    def test_open_file_not_exist(self):
        with self.assertRaises(SystemExit) as cm:
            open_file('file_not_exist')
            self.assertEqual(cm.exception, '1')
