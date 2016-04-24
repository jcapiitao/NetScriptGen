# -*-coding:UTF-8 -*
import sys
import traceback
import re
from collections import OrderedDict

class ArrayParsing(object):
    """"
    This class is used to parse a sheet which contains an array.

    ..  note::
        By default, if the cell A1 doesn't contain the words 'List' or 'Text', then the sheet
        is considered as an Array.

    """
    # TODO finalise la description de la classe

    def __init__(self, xl_sheet):
        self.xl_sheet = xl_sheet
        self.sheet_name = xl_sheet.name
        self.commands = self.get_local_templates()
        self.index = dict()
        self.tb = list()

        is_duplication, indexes_duplicated = self.is_duplication(self.get_all_indexes())
        if is_duplication is True:
            raise SystemExit("The index(es) in sheet '%s' are duplicated: %s" %
                             (self.sheet_name, indexes_duplicated))

        is_duplication, headers_duplicated = self.is_duplication(self.get_all_headers())
        if is_duplication is True:
            raise SystemExit("The parameter(s) in sheet '%s' are duplicated: %s" %
                             (self.sheet_name, headers_duplicated))

        for row_idx in range(1, xl_sheet.nrows):
            index_obj = xl_sheet.cell(row_idx, 0)
            index_value = self.to_string(index_obj)
            self.index[index_value] = dict()
            for col_idx in range(0, self.get_nbr_of_cols_in_row(0)):
                param_obj = xl_sheet.cell(0, col_idx)
                param_value = self.to_string(param_obj)
                var_obj = self.xl_sheet.cell(row_idx, col_idx)
                var_value = self.to_string(var_obj)
                self.index[index_value][param_value] = var_value

    def get_value_of_var_by_index_and_param(self, index_value, param_value):
        try:
            return self.index[index_value][param_value]
        except KeyError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            output = "The index '{0}' or the parameter '{1}' " \
                     "doesn't exist in the worksheet '{2}'".format(index_value, param_value, self.sheet_name)
            print(output)
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            raise KeyError(output)

    def set_value_by_index_and_param(self, index_value, param_value, updated_value):
        try:
            self.index[index_value][param_value] = updated_value
        except KeyError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            output = "The index '{0}' or the parameter '{1}' " \
                     "doesn't exist in the worksheet '{2}'".format(index_value, param_value, self.sheet_name)
            print(output)
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            raise KeyError(output)

    def get_all_param_by_index(self, index_value):
        dict_of_params = OrderedDict()
        for param_value in self.get_all_headers():
            dict_of_params[str(param_value)] = self.get_value_of_var_by_index_and_param(index_value, param_value)
        return dict_of_params

    def display_param_by_index(self, index_value, param_value):
        print(self.get_value_of_var_by_index_and_param(index_value, param_value))

    def get_nbr_of_rows(self):
        return self.xl_sheet.nrows

    def get_nbr_of_cols(self):
        return self.xl_sheet.ncols

    def get_nbr_of_cols_in_row(self, row):
        return self.xl_sheet.row_len(row)

    def get_all_headers(self):
        list_of_headers = list()
        for col_idx in range(0, self.get_nbr_of_cols_in_row(0)):
            header_obj = self.xl_sheet.cell(0, col_idx)
            header_value = self.to_string(header_obj)
            list_of_headers.append(header_value)
        return list_of_headers

    def get_all_indexes(self):
        indexes = list()
        for row_idx in range(1, self.delimitation_between_indexes_and_commands()):
            index_obj = self.xl_sheet.cell(row_idx, 0)
            index_value = self.to_string(index_obj)
            indexes.append(index_value)
        for iterator in range(0, indexes.count('')):
            indexes.remove('')
        return indexes

    def template_content_by_name(self, name):
        for row_idx in range(self.delimitation_between_indexes_and_commands(), self.get_nbr_of_rows()):
            template_name_obj = self.xl_sheet.cell(row_idx, 0)
            template_name = self.to_string(template_name_obj)
            if template_name.lower() == name:
                template_content_obj = self.xl_sheet.cell(row_idx + 1, 0)
                return self.to_string(template_content_obj)

    def get_row_where_value(self, value):
        for row_idx in range(1, self.xl_sheet.nrows):
            cell_obj = self.xl_sheet.cell(row_idx, 0)
            cell_value = self.to_string(cell_obj)
            if cell_value == str(value):
                return row_idx
        return -1

    def delimitation_between_indexes_and_commands(self):
        row_idx = self.get_row_where_value('Default')
        if row_idx == -1:
            return self.get_nbr_of_rows()
        else:
            return row_idx

    @staticmethod
    def is_duplication(key_list):
        response = list()
        for key in key_list:
            count = key_list.count(str(key))
            if count > 1 and key not in response and key != '':
                response.append(key)
        if len(response) == 0:
            return False, response
        else:
            return True, response

    @staticmethod
    def to_string(cell_obj):
        # Integer values in Excel are imported as floats in Python.
        # So we have to convert floats (2, 3) into integer
        if cell_obj.ctype in (2, 3):
            cell_value = int(cell_obj.value)
            return str(cell_value)
        else:
            return str(cell_obj.value)
