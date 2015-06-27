#!/usr/bin/python3
# -*-coding:UTF-8 -*

from unittest import TestCase
from process.ArrayParsing import ArrayParsing
from src.unittest.python.ExcelFile import *

class ArrayParsingTests(TestCase):

    def setUp(self):
        self.sheet = ArrayParsing(getSheet('VLAN'))
        print('setUp')

    def test_get_param_by_index(self):
        self.assertEqual(self.sheet.get_param_by_index('105', 'Gateway'), '10.2.2.254')

    def test_set_param_by_index(self):
        index_value, param_value, updated_value = '104', 'Gateway', '1.1.1.1'
        self.sheet.set_param_by_index(index_value, param_value, updated_value )
        self.assertEqual(self.sheet.get_param_by_index(index_value, param_value), updated_value)



"""
vlan = ArrayParsing(my_sheet)
vlan.display_param_by_index('11', 'Gateway')
vlan.set_param_by_index('11', 'Gateway', '1.1.1.1')
vlan.display_param_by_index('11', 'Gateway')
print(vlan.get_nbr_of_rows())
print(vlan.get_nbr_of_cols())
print(vlan.get_headers())

user = ArrayParsing(wb.sheet_by_name('User'))
user.display_param_by_index('ultime','Password')
"""