# -*-coding:UTF-8 -*

from unittest import TestCase
from equipment.feature.Interface import Interface
from utils.ExcelWorkbookManager import get_sheet


class InterfaceTests(TestCase):

    interface = Interface(get_sheet('interface_test'))

    def test_get_by_equipment_and_function(self):
        ref_list = ['Gigabit', '1', '0', '1-2']
        self.assertListEqual(ref_list, self.interface.get_by_equipment_and_function('CISCO WS-C3750v2-48PS-S', 'Uplink'))

    def test_get_by_equipment_and_function_in_stack(self):
        value_expected = 'Gigabit 1/0/1-2,Gigabit 2/0/1-2,Gigabit 3/0/1-2'
        self.assertEqual(value_expected, self.interface.get_by_equipment_and_function_in_stack('CISCO WS-C3750v2-48PS-S', 'Uplink', 3))

    def test_in_string(self):
        value_expected = 'Gigabit 1/0/1-2'
        list = ['Gigabit', '1', '0', '1-2']
        self.assertEqual(value_expected, self.interface.in_string(list))