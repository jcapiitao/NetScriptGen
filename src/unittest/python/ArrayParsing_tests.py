#!/usr/bin/python3
# -*-coding:UTF-8 -*

from unittest import TestCase
from process.ArrayParsing import ArrayParsing
from src.unittest.python.ExcelFile import *

class ArrayParsingTests(TestCase):

    def setUp(self):
        self.sheet = ArrayParsing(getSheet('arrayparsing_test'))
        print('setUp')

    def test_get_param_by_index(self):
        self.assertEqual(self.sheet.get_param_by_index('105', 'Gateway'), '10.2.2.254')

    def test_set_param_by_index(self):
        index_value, param_value, updated_value = '104', 'Gateway', '1.1.1.1'
        self.sheet.set_param_by_index(index_value, param_value, updated_value )
        self.assertEqual(self.sheet.get_param_by_index(index_value, param_value), updated_value)

    def test_get_all_param_by_index(self):
        ref_dict = {'Vlans ID': '105', 'Name': 'VLAN-VOICE-02', 'Subnet': '10.2.2.0', 'Mask': '255.255.255.0', 'Gateway': '10.2.2.254',
                    'Description': '', 'Subnet_arp': '10.2.2.224', 'Wildcard_arp': '0.0.0.15'}
        self.assertDictEqual(ref_dict, self.sheet.get_all_param_by_index('105'))

    def test_get_nbr_of_rows(self):
        self.assertEqual(self.sheet.get_nbr_of_rows(), 16)

    def test_get_nbr_of_cols(self):
        self.assertEqual(self.sheet.get_nbr_of_cols(), 8)


"""
print(vlan.get_headers())

user = ArrayParsing(wb.sheet_by_name('User'))
user.display_param_by_index('ultime','Password')
"""