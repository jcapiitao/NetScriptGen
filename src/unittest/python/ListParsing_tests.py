# -*-coding:UTF-8 -*

from unittest import TestCase
from process.ListParsing import ListParsing
from utils.ExcelWorkbookManager import get_sheet_test


class ListParsingTests(TestCase):

    def setUp(self):
        self.sheet = ListParsing(get_sheet_test('listparsing_test.xlsx'))

    def test_get_value_by_bag_and_key(self):
        values = list()
        self.assertListEqual(self.sheet.get_value_by_bag_and_key('Administrative', 'Code Site'), values)

    def test_get_value_by_bag_and_key_and_index(self):
        expected = '45'
        got = self.sheet.get_value_by_bag_and_key_and_index('Administrative', 'Num Site', 1)
        self.assertEqual(expected, got)

    def test_get_value_by_bag_and_key_and_index_failed(self):
        expected = IndexError
        got = self.sheet.get_value_by_bag_and_key_and_index('Administrative', 'Num Site', 5)
        self.assertRaises(expected, got)

    def test_get_param_by_index_failed(self):
        expected = KeyError
        got = self.sheet.get_value_by_bag_and_key('invalid_bag', 'invalid_key')
        self.assertRaises(expected, got)

    def test_set_value_by_bag_and_key(self):
        bag, key, updated_value = 'DNS', 'DNS Server', '1.1.1.1'
        expected = list()
        expected.append(updated_value)
        self.sheet.set_value_by_bag_and_key(bag, key, 1, updated_value)
        got = self.sheet.get_value_by_bag_and_key(bag, key)
        self.assertListEqual(expected, got)

    def test_set_value_by_bag_and_key_failed(self):
        bag, key, updated_value = '000', 'Gateway', '1.1.1.1'
        expected = KeyError
        got = self.sheet.set_value_by_bag_and_key(bag, key, 0, updated_value)
        self.assertRaises(expected, got)

    def test_get_all_keys_by_bag(self):
        expected = ['Radius Server 1', 'Radius Server 2']
        got = sorted(self.sheet.get_all_keys_by_bag('Authentication'))
        self.assertListEqual(expected, got)

    def test_get_all_keys_by_bag_failed(self):
        expected = KeyError
        got = self.sheet.get_all_keys_by_bag('invalid_bag')
        self.assertRaises(expected, got)

    def test_get_all_keys(self):
        expected = ['Code Site', 'Num Site', 'AS Number', 'DNS Domain-name', 'DNS Server', 'DNS Server 2',
                    'DHCP Relay 1', 'DHCP Relay 2', '123', 'Radius Server 1', 'Radius Server 2']
        expected = sorted(expected)
        got = sorted(self.sheet.get_all_keys())
        self.assertListEqual(expected, got)

    def test_get_value_by_key(self):
        expected = list()
        expected.append('65845')
        got = self.sheet.get_value_by_key('AS Number')
        self.assertListEqual(expected, got)

    def test_get_value_by_key_failed(self):
        expected = KeyError
        got = self.sheet.get_value_by_key('invalid_key')
        self.assertRaises(expected, got)

    def test_set_value_by_key(self):
        key, index, updated_value = 'Radius Server 1', 1, '1.1.1.1'
        expected = list()
        expected.append(updated_value)
        self.sheet.set_value_by_key(key, index, updated_value)
        got = self.sheet.get_value_by_key(key)
        self.assertListEqual(expected, got)

    def test_set_value_by_key_failed(self):
        expected = KeyError
        got = self.sheet.set_value_by_key('invalid_key', 1, '1.1.1.1')
        self.assertRaises(expected, got)
