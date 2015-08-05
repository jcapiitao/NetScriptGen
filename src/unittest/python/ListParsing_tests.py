# -*-coding:UTF-8 -*

from unittest import TestCase
from process.ListParsing import ListParsing
from utils.ExcelWorkbookManager import get_sheet


class ListParsingTests(TestCase):

    sheet = ListParsing(get_sheet('listparsing_test'))

    def test_get_value_by_bag_and_key(self):
        values = list()
        self.assertListEqual(self.sheet.get_value_by_bag_and_key('Administrative', 'Code Site'), values)

    def test_get_value_by_bag_and_key_and_index(self):
        self.assertEqual(self.sheet.get_value_by_bag_and_key_and_index('Administrative', 'Num Site', 1), '45')

    def test_get_value_by_bag_and_key_and_index_failed(self):
        self.assertRaises(IndexError, self.sheet.get_value_by_bag_and_key_and_index('Administrative', 'Num Site', 5))

    def test_get_param_by_index_failed(self):
        self.assertRaises(KeyError, self.sheet.get_value_by_bag_and_key('invalid_bag', 'invalid_key'))

    def test_set_value_by_bag_and_key(self):
        bag, key, updated_value = 'DNS', 'DNS Server', '1.1.1.1'
        values = list()
        values.append(updated_value)
        self.sheet.set_value_by_bag_and_key(bag, key, 1, updated_value)
        self.assertListEqual(self.sheet.get_value_by_bag_and_key(bag, key), values)

    def test_set_value_by_bag_and_key_failed(self):
        bag, key, updated_value = '000', 'Gateway', '1.1.1.1'
        self.assertRaises(KeyError, self.sheet.set_value_by_bag_and_key(bag, key, 0, updated_value))

    def test_get_all_keys_by_bag(self):
        ref_list = ['Radius Server 1', 'Radius Server 2']
        ref_list = sorted(ref_list)
        self.assertListEqual(ref_list, sorted(self.sheet.get_all_keys_by_bag('Authentication')))

    def test_get_all_keys_by_bag_failed(self):
        self.assertRaises(KeyError, self.sheet.get_all_keys_by_bag('invalid_bag'))

    def test_get_all_keys(self):
        ref_list = ['Code Site', 'Num Site', 'AS Number', 'DNS Domain-name', 'DNS Server', 'DNS Server 2',
                    'DHCP Relay 1', 'DHCP Relay 2', '123', 'Radius Server 1', 'Radius Server 2']
        ref_list = sorted(ref_list)
        self.assertListEqual(ref_list, sorted(self.sheet.get_all_keys()))

    def test_get_value_by_key(self):
        values = list()
        values.append('65845')
        self.assertListEqual(self.sheet.get_value_by_key('AS Number'), values)

    def test_get_value_by_key_failed(self):
        self.assertRaises(KeyError, self.sheet.get_value_by_key('invalid_key'))

    def test_set_value_by_key(self):
        key, index, updated_value = 'Radius Server 1', 1, '1.1.1.1'
        values = list()
        values.append(updated_value)
        self.sheet.set_value_by_key(key, index, updated_value)
        self.assertListEqual(self.sheet.get_value_by_key(key), values)

    def test_set_value_by_key_failed(self):
        self.assertRaises(KeyError, self.sheet.set_value_by_key('invalid_key', 1, '1.1.1.1'))

    def test_is_key_in_list_True(self):
        self.assertEqual(self.sheet.is_key('123'), True)

    def test_is_key_in_list_False(self):
        self.assertEqual(self.sheet.is_key('000'), False)
