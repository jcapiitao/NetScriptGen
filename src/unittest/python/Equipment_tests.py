from unittest import TestCase
from equipment.Equipment import Equipment
from process.ArrayParsing import ArrayParsing
from process.ListParsing import ListParsing
from process.TextParsing import TextParsing
from utils.ExcelWorkbookManager import get_sheet_test


class EquipmentTests(TestCase):

    def setUp(self):
        array_test, list_test = 'arrayParsing_test', 'listParsing_test'
        text_test, global_test = 'textParsing_test', 'global_test'
        my_template = "{{hostname}}\n{{VLAN}}\n{{VLAN!((VLAN!104:Name)):Gateway}}"
        self.workbook = dict()
        self.workbook['VLAN'] = ArrayParsing(get_sheet_test(array_test + '.xlsx'))
        self.workbook[list_test] = ListParsing(get_sheet_test(list_test + '.xlsx'))
        self.workbook[text_test] = TextParsing(get_sheet_test(text_test + '.xlsx'))
        self.workbook['Global'] = ArrayParsing(get_sheet_test(global_test + '.xlsx'))
        self.equipment = Equipment('HOST1', my_template, self.workbook)
        self.equipment.unresolved = 1
        self.equipment.resolved = 2

    def test_fill_out_the_template(self):
        expected = "HOST1\nADMRESEAU-1 and 10.1.255.0 and\n10.179.255.6210.1.0.224\n0.0.0.15\n10.1.1.254"
        got = self.equipment.fill_out_the_template()
        self.assertEqual(expected, got)

    def test_get_value_of_var_1(self):
        var_to_fill = 'VLAN!41:Name'
        expected = 'ADMWIFI-1'
        got = self.equipment.get_value_of_var(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_get_value_of_var_2(self):
        var_to_fill = 'Equipment'
        expected = 'CISCO 3750 V3-48PS'
        got = self.equipment.get_value_of_var(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_get_value_of_var_with_interrogation(self):
        var_to_fill = 'VLAN?Name'
        expected = 'ADMRESEAU-1'
        got = self.equipment.get_value_of_var(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_get_value_of_var_with_interrogation_unresolved(self):
        var_to_fill = 'Are you ok? Yep'
        expected = '<unresolved>'
        got = self.equipment.get_value_of_var(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_get_var_from_global_sheet_is_sheet(self):
        expected = 'ADMRESEAU-1 and 10.1.255.0 and\n10.179.255.6210.1.0.224\n0.0.0.15'
        got = self.equipment.get_value_of_var_from_global_sheet('VLAN')
        self.assertEqual(expected, got)

    def test_get_var_from_global_sheet_is_var(self):
        expected = 'CISCO 3750 V3-48PS'
        got = self.equipment.get_value_of_var_from_global_sheet('Equipment')
        self.assertEqual(expected, got)

    def test_get_var_with_exclamation_and_colon_ArrayParsing(self):
        var_to_fill = 'VLAN!((VLAN!104:Name)):Gateway'
        expected = '10.1.1.254'
        got = self.equipment.get_value_of_var_with_exclamation_and_colon(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_get_var_with_exclamation_and_colon_ArrayParsing_unresolved(self):
        var_to_fill = 'VLAN!((VLAN!Parcher:Name)):Gateway'
        expected = '<unresolved>'
        got = self.equipment.get_value_of_var_with_exclamation_and_colon(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_get_var_with_exclamation_and_colon_ListParsing(self):
        var_to_fill = 'listParsing_test!DNS:DNS Server:1'
        expected = '10.100.10.1'
        got = self.equipment.get_value_of_var_with_exclamation_and_colon(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_get_var_with_exclamation_and_colon_ListParsing_unresolved(self):
        var_to_fill = 'listParsing_test!MalCobbs:DNS Server:1'
        expected = '<unresolved>'
        got = self.equipment.get_value_of_var_with_exclamation_and_colon(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_get_var_with_exclamation_and_colon_TextParsing(self):
        var_to_fill = 'textParsing_test!banner'
        expected = 'test'
        got = self.equipment.get_value_of_var_with_exclamation_and_colon(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_get_var_with_exclamation_and_colon_TextParsing_unresolved(self):
        var_to_fill = 'textParsing_test!TylerDurden'
        expected = '<unresolved>'
        got = self.equipment.get_value_of_var_with_exclamation_and_colon(var_to_fill, self.workbook)
        self.assertEqual(expected, got)

    def test_remove_brackets(self):
        expected = "Wuce Brayne"
        got = self.equipment.remove_braces("{{Wuce Brayne}}")
        self.assertEqual(expected, got)

    def test_get_filling_ratio_in_percentage(self):
        expected = '67%'
        got = self.equipment.get_filling_ratio_in_percentage()
        self.assertEqual(expected, got)

    def test_get_filling_ratio(self):
            expected = '2/3'
            got = self.equipment.get_filling_ratio()
            self.assertEqual(expected, got)

    def test_get_nbr_of_var_to_fill_in(self):
            expected = 3
            got = self.equipment.get_nbr_of_var_to_fill_in()
            self.assertEqual(expected, got)