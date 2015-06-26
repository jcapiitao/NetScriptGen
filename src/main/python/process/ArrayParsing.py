#!/usr/bin/python3
# -*-coding:UTF-8 -*

import sys
import xlrd
from xlrd.sheet import ctype_text
from os.path import join, dirname, abspath


class ArrayParsing(object):
    def __init__(self, xl_sheet):

        self.xl_sheet = xl_sheet
        self.sheet_name = xl_sheet.name
        self.commands = self.get_all_commands()
        self.index = dict()

        index_list = self.is_doublon(self.get_all_indexes())
        if index_list[0] is True:
            print("The index(es) in tab '%s' are duplicated: %s" % (self.sheet_name, index_list[1:]))

        header_list = self.is_doublon(self.get_all_headers())
        if header_list[0] is True:
            print("The parameter in tab '%s' are duplicated: %s" % (self.sheet_name, header_list[1:]))

        for row_idx in range(1, xl_sheet.nrows):
            idx_value_obj = xl_sheet.cell(row_idx, 0)

            if idx_value_obj.ctype in (2, 3):
                idx_value = int(idx_value_obj.value)
            else:
                idx_value = idx_value_obj.value

            if (idx_value == 'Default'):
                self.commands[idx_value] = xl_sheet.cell(row_idx + 1, 0)

            else:
                self.index[str(idx_value)] = dict()
                for col_idx in range(0, xl_sheet.ncols):
                    var_obj = xl_sheet.cell(row_idx, col_idx)
                    if var_obj.ctype in (2, 3):
                        var_obj = int(var_obj.value)
                    else:
                        var_obj = var_obj.value
                    param_value = str(xl_sheet.cell(0, col_idx).value)
                    self.index[str(idx_value)][param_value] = var_obj


    def get_param_by_index(self, index_value, param_value):
        try:
            return self.index[index_value][param_value]
        except KeyError:
            print("The index '%s' or the parameter '%s' doesn't exist in the tab '%s'." \
                  % (index_value, param_value, self.sheet_name))

    def set_param_by_index(self, index_value, param_value, updated_value):
        self.index[index_value][param_value] = updated_value

    def get_all_param_by_index(self, index_value):
        my_dict = dict()
        for param in self.get_all_headers():
            my_dict[str(param)] = self.get_param_by_index(index_value, param)
        return my_dict

    def display_param_by_index(self, index_value, param_value):
        print(self.get_param_by_index(index_value, param_value))

    def get_nbr_of_rows(self):
        return self.xl_sheet.nrows

    def get_nbr_of_cols(self):
        return self.xl_sheet.ncols

    def get_all_headers(self):
        headers = list()
        for col_idx in range(0, self.get_nbr_of_cols()):
            headers.append(str(self.xl_sheet.cell(0, col_idx).value))
        return headers

    def get_all_indexes(self):
        indexes = list()
        for row_idx in range(1, self.get_nbr_of_rows()):
            index_obj = self.xl_sheet.cell(row_idx, 0)
            if index_obj.ctype in (2, 3):
                index_value = int(index_obj.value)
            else:
                index_value = index_obj.value
            indexes.append(str(index_value))
        return indexes

    def is_key_in_list(self, key, list):
        if key in list:
            return True
        else:
            return False

    def is_doublon(self, key_list):
        response = list()
        for key in key_list:
            count = key_list.count(str(key))
            if count > 1 and not key in response and key != '':
                response.append(key)
        if len(response) == 0:
            response.append(False)
        else:
            response.insert(0, True)
        return response

    def get_all_commands(self):
        commands = dict()
        command_row = self.get_row_where_value('Default')
        if command_row != 0:
            for row_idx in range(command_row, self.get_nbr_of_rows(), 2):
                idx_value_obj = self.xl_sheet.cell(row_idx, 0)
                if idx_value_obj.ctype in (2, 3):
                    idx_value = int(idx_value_obj.value)
                else:
                    idx_value = idx_value_obj.value
                if (idx_value != ""):
                    commands[idx_value] = str(self.xl_sheet.cell(row_idx + 1, 0).value)
            return commands


    def get_row_where_value(self, value):
        for row_idx in range(1, self.xl_sheet.nrows):
            idx_value_obj = self.xl_sheet.cell(row_idx, 0)

            if idx_value_obj.ctype in (2, 3):
                idx_value = int(idx_value_obj.value)
            else:
                idx_value = idx_value_obj.value

            if idx_value == value:
                return row_idx
        return 0


"""
fname = "C:/Users/joec/Desktop/joware/joware-v2/test.xlsx"
wb = xlrd.open_workbook(fname)
my_sheet = wb.sheet_by_name('VLANs')

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