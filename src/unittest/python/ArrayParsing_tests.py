#!/usr/bin/python3
# -*-coding:UTF-8 -*

from unittest import TestCase

from process.ArrayParsing import ArrayParsing
from utils.ExcelFile import getSheet


class ArrayParsingTests(TestCase):

    sheet = ArrayParsing(getSheet('arrayparsing_test'))

    def test_get_param_by_index(self):
        self.assertEqual(self.sheet.get_param_by_index('105', 'Gateway'), '10.2.2.254')

    def test_get_param_by_index_failed(self):
        self.assertRaises(KeyError, self.sheet.get_param_by_index('200', 'invalid_param'))

    def test_set_param_by_index(self):
        index_value, param_value, updated_value = '104', 'Gateway', '1.1.1.1'
        self.sheet.set_param_by_index(index_value, param_value, updated_value )
        self.assertEqual(self.sheet.get_param_by_index(index_value, param_value), updated_value)

    def test_set_param_by_index_failed(self):
        index_value, param_value, updated_value = '000', 'Gateway', '1.1.1.1'
        self.assertRaises(KeyError, self.sheet.set_param_by_index(index_value, param_value, updated_value))

    def test_get_all_param_by_index(self):
        ref_dict = {'Vlans ID': '105', 'Name': 'VLAN-VOICE-02', 'Subnet': '10.2.2.0', 'Mask': '255.255.255.0', 'Gateway': '10.2.2.254',
                    'Description': '', 'Subnet_arp': '10.2.2.224', 'Wildcard_arp': '0.0.0.15'}
        self.assertDictEqual(ref_dict, self.sheet.get_all_param_by_index('105'))

    def test_get_nbr_of_rows(self):
        self.assertEqual(self.sheet.get_nbr_of_rows(), 35)

    def test_get_nbr_of_cols(self):
        self.assertEqual(self.sheet.get_nbr_of_cols(), 8)

    def test_get_all_headers(self):
        ref_list = ['Vlans ID', 'Name', 'Subnet', 'Mask', 'Gateway', 'Description', 'Subnet_arp', 'Wildcard_arp']
        self.assertListEqual(ref_list, self.sheet.get_all_headers())

    def test_get_all_indexes(self):
        ref_list = ['21', '22', '23', '41', '42', '43', '101', '102', '103', '104', '105', '106', '107', '108', '109']
        self.assertListEqual(ref_list, self.sheet.get_all_indexes())

    def test_is_key_in_list(self):
        self.assertEqual(self.sheet.is_key_in_list('21', self.sheet.get_all_indexes()), True)

    def test_is_duplication_False(self):
        ref_list = [False]
        self.assertListEqual(ref_list, self.sheet.is_duplication(self.sheet.get_all_headers()))

    def test_get_all_commands(self):
        ref_dict =  {'Default': 'test', 'Snooping': 'test', 'Inspection': 'test'}
        self.assertDictEqual(ref_dict, self.sheet.get_all_commands())

    def test_get_row_where_value(self):
        self.assertEqual(self.sheet.get_row_where_value(105), 11)

    def test_get_row_where_value_failed(self):
        self.assertEqual(self.sheet.get_row_where_value(0000), -1)
