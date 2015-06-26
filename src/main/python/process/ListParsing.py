#!/usr/bin/python3
# -*-coding:UTF-8 -*

import sys
import xlrd, time
from xlrd.sheet import ctype_text
from os.path import join, dirname, abspath


class ListParsing(object):
    global my_dict, my_dict2
    my_dict = dict()
    my_dict2 = dict()

    def __init__(self, xl_sheet):

        for row_idx in range(1, xl_sheet.nrows):
            self.xl_sheet = xl_sheet
            self.sheet_name = xl_sheet.name

            bag_obj = xl_sheet.cell(row_idx, 0)
            bag = bag_obj.value
            key_obj = xl_sheet.cell(row_idx, 1)
            value_obj = xl_sheet.cell(row_idx, 2)

            # Integer values in Excel are imported as floats in Python.
            # So we have to convert floats (2, 3) into integer
            if value_obj.ctype in (2, 3):
                value = int(value_obj.value)
            else:
                value = value_obj.value

            if not bag in my_dict.keys():
                my_dict[bag] = dict()

            my_dict2[key_obj.value] = value
            my_dict[bag][key_obj.value] = value

    def get_value_by_bag_and_key(self, bag, key):
        try:
            return my_dict[bag][key]
        except KeyError:
            print("The bag '%s' or the key '%s' doesn't exist in the tab '%s'." \
                  % (bag, key, self.sheet_name))

    def set_value_by_bag_and_key(self, bag, key, value):
        my_dict[bag][key] = value

    def display_value_by_bag_and_key(self, bag, key):
        print(self.get_value_by_bag_and_key(bag, key))

    def get_all_keys_by_bag(self, bag):
        return my_dict[bag].keys()

    def get_all_keys(self):
        return my_dict2.keys()

    def get_value_by_key(self, key):
        return my_dict2[key]

    def set_value_by_key(self, key, value):
        my_dict2[key] = value

    def is_key(self, key):
        keys_list = self.get_all_keys()
        if key in keys_list:
            return True
        else:
            return False


"""
fname = "C:/Users/joec/Desktop/joware/joware-v2/test.xlsx"
wb = xlrd.open_workbook(fname)
my_sheet = wb.sheet_by_name('liste')

config = ListParsing(my_sheet)
config.display_value_by_bag_and_key('DNS', 'DNS Server 1')
config.set_value_by_bag_and_key('DNS', 'DNS Server 1', '1.1.1.1')
print(config.is_key('pouet'))
print(config.is_key('DNS Server 1'))
print(config.get_all_keys_by_bag('DNS'))
config.display_value_by_bag_and_key('DNS', 'DNS Server 1')
"""