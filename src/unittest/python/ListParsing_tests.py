# -*-coding:UTF-8 -*

from unittest import TestCase
from process.ListParsing import ListParsing
from utils.ExcelFile import getSheet


class ListParsingTests(TestCase):

    sheet = ListParsing(getSheet('listparsing_test'))

    def test_get_value_by_bag_and_key(self):
        self.assertEqual(self.sheet.get_value_by_bag_and_key('Administrative', 'Code Site'), '')

    def test_get_param_by_index_failed(self):
        self.assertRaises(KeyError, self.sheet.get_value_by_bag_and_key('invalid_bag', 'invalid_key'))

    def test_set_value_by_bag_and_key(self):
        bag, key, updated_value = 'DNS', 'DNS Server 1', '1.1.1.1'
        self.sheet.set_value_by_bag_and_key(bag, key, updated_value)
        self.assertEqual(self.sheet.get_value_by_bag_and_key(bag, key), updated_value)

    def test_set_value_by_bag_and_key_failed(self):
        bag, key, updated_value = '000', 'Gateway', '1.1.1.1'
        self.assertRaises(KeyError, self.sheet.set_value_by_bag_and_key(bag, key, updated_value))

    def test_get_all_keys_by_bag(self):
        ref_list = ['Radius Server 1', 'Radius Server 2']
        ref_list = sorted(ref_list)
        self.assertListEqual(ref_list, sorted(self.sheet.get_all_keys_by_bag('Authentication')))

    def test_get_all_keys_by_bag_failed(self):
        self.assertRaises(KeyError, self.sheet.get_all_keys_by_bag('invalid_bag'))

    def test_get_all_keys(self):
        ref_list = ['Code Site', 'Num Site', 'AS Number', 'DNS Domain-name', 'DNS Server 1', 'DNS Server 2',
                    'DHCP Relay 1', 'DHCP Relay 2', '123', 'Radius Server 1', 'Radius Server 2']
        ref_list = sorted(ref_list)
        self.assertListEqual(ref_list, sorted(self.sheet.get_all_keys()))

    def test_get_value_by_key(self):
        self.assertEqual(self.sheet.get_value_by_key('AS Number'), '65845')

    def test_get_value_by_key_failed(self):
        self.assertRaises(KeyError, self.sheet.get_value_by_key('invalid_key'))

    def test_set_value_by_key(self):
        self.sheet.set_value_by_key('Radius Server 1', '1.1.1.1')
        self.assertEqual(self.sheet.get_value_by_key('Radius Server 1'), '1.1.1.1')

    def test_set_value_by_key_failed(self):
        self.assertRaises(KeyError, self.sheet.set_value_by_key('invalid_key', '1.1.1.1'))

    def test_is_key_in_list_True(self):
        self.assertEqual(self.sheet.is_key('123'), True)

    def test_is_key_in_list_False(self):
        self.assertEqual(self.sheet.is_key('000'), False)
