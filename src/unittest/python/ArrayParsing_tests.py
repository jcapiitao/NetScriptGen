# -*-coding:UTF-8 -*

from unittest import TestCase
from process.ArrayParsing import ArrayParsing
from utils.ExcelWorkbookManager import get_sheet_test

class ArrayParsingTests(TestCase):

    def setUp(self):
        self.sheet = ArrayParsing(get_sheet_test('arrayParsing_test.xlsx'))

    def test_get_param_by_index(self):
        expected = '10.2.2.254'
        got = self.sheet.get_value_of_var_by_index_and_param('105', 'Gateway')
        self.assertEqual(expected, got)

    def test_get_param_by_index_failed(self):
        expected = KeyError
        got = self.sheet.get_value_of_var_by_index_and_param('101', 'invalid_param')
        self.assertRaises(expected, got)

    def test_set_param_by_index(self):
        index_value, param_value, updated_value = '104', 'Gateway', '1.1.1.1'
        self.sheet.set_value_by_index_and_param(index_value, param_value, updated_value)
        got = self.sheet.get_value_of_var_by_index_and_param(index_value, param_value)
        self.assertEqual(updated_value, got)

    def test_set_param_by_index_failed(self):
        index_value, param_value, updated_value = '000', 'Gateway', '1.1.1.1'
        expected = KeyError
        got = self.sheet.set_value_by_index_and_param(index_value, param_value, updated_value)
        self.assertRaises(expected, got)

    def test_get_all_param_by_index(self):
        expected = {'Vlans ID': '105',
                    'Name': 'VLAN-VOICE-02',
                    'Subnet': '10.2.2.0',
                    'Mask': '255.255.255.0',
                    'Gateway': '10.2.2.254',
                    'Description': '',
                    'Subnet_arp': '10.2.2.224',
                    'Wildcard_arp': '0.0.0.15',
                    'Template Default': 'Non',
                    'Template Snooping': 'Non',
                    'Template Inspection': 'Non'}
        got = self.sheet.get_all_param_by_index('105')
        self.assertDictEqual(expected, got)

    def test_get_nbr_of_rows(self):
        expected = 23
        got = self.sheet.get_nbr_of_rows()
        self.assertEqual(expected, got)

    def test_get_nbr_of_cols(self):
        expected = 11
        got = self.sheet.get_nbr_of_cols()
        self.assertEqual(expected, got)

    def test_get_nbr_of_cols_in_row(self):
        expected = 11
        got = self.sheet.get_nbr_of_cols_in_row(0)
        self.assertEquals(expected, got)

    def test_get_all_headers(self):
        expected = ['Vlans ID', 'Name', 'Subnet', 'Mask', 'Gateway', 'Description', 'Subnet_arp', 'Wildcard_arp',
                    'Template Default', 'Template Snooping', 'Template Inspection']
        got = self.sheet.get_all_headers()
        self.assertListEqual(expected, got)

    def test_get_all_indexes(self):
        expected = ['21', '22', '23', '41', '42', '43', '101', 'test', '103', '104', '105', '106', '107', '108', '109']
        got = self.sheet.get_all_indexes()
        self.assertListEqual(expected, got)

    def test_is_duplication_False(self):
        expected = (False, [])
        got = self.sheet.is_duplication(self.sheet.get_all_headers())
        self.assertEqual(expected, got)

    def test_is_duplication_True(self):
        list_of_superheroes = ['Superman', 'Superman', 'Superman', 'Batman', 'Batman', 'Ironman', 'Thor']
        expected = (True, ['Superman', 'Batman'])
        got = self.sheet.is_duplication(list_of_superheroes)
        self.assertEqual(expected, got)

    def test_get_all_commands(self):
        expected = [('Default', '{{Name}} and {{Subnet}} and\n{{Gateway}}'),
                    ('Snooping', '{{Subnet_arp}}\n{{Wildcard_arp}}'),
                    ('Inspection', '')]
        got = self.sheet.get_local_templates()
        self.assertListEqual(expected, got)

    def test_get_row_where_value(self):
        expected = 11
        got = self.sheet.get_row_where_value(105)
        self.assertEqual(expected, got)

    def test_get_row_where_value_failed(self):
        expected = -1
        got = self.sheet.get_row_where_value(0000)
        self.assertEqual(expected, got)

    def test_delimitation_between_indexes_and_commands(self):
        expected = 17
        got = self.sheet.delimitation_between_indexes_and_commands()
        self.assertEqual(expected, got)
