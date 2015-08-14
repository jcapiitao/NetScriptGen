# -*-coding:UTF-8 -*


class ListParsing(object):
    # TODO Description of the class and its method

    def __init__(self, xl_sheet):
        self.xl_sheet = xl_sheet
        self.sheet_name = xl_sheet.name
        self.my_dict = dict()
        self.my_dict2 = dict()
        for row_idx in range(1, xl_sheet.nrows):
            value = list()
            bag_cell = xl_sheet.cell(row_idx, 0)
            bag = str(self.if_float_convert_to_int(bag_cell))
            key_cell = xl_sheet.cell(row_idx, 1)
            key = str(self.if_float_convert_to_int(key_cell))
            col_idx = 2
            while col_idx < xl_sheet.ncols:
                if xl_sheet.cell(row_idx, col_idx).ctype not in (0, 6):
                    value_cell = xl_sheet.cell(row_idx, col_idx)
                    value.append(str(self.if_float_convert_to_int(value_cell)))
                col_idx += 1
            if bag not in self.my_dict.keys():
                self.my_dict[bag] = dict()
            self.my_dict2[key] = value
            self.my_dict[bag][key] = value

    def get_value_by_bag_and_key(self, bag, key):
        try:
            return self.my_dict[bag][key]
        except KeyError:
            print("The bag '%s' or the key '%s' doesn't exist in the tab '%s'." % (bag, key, self.sheet_name))

    def get_value_by_bag_and_key_and_index(self, bag, key, index):
        try:
            values = self.get_value_by_bag_and_key(bag, key)
            try:
                if values:
                    return values[index-1]
            except IndexError:
                print("There is no such index in the list '%s->%s = %s'" % (bag, key, values))
        except KeyError:
            print("The index '%s' doesn't exist in the tab '%s'." % (index, self.sheet_name))

    def set_value_by_bag_and_key(self, bag, key, index, value):
        try:
            index -= 1
            list_bag_and_key = self.my_dict[bag][key]
            if list_bag_and_key:
                list_bag_and_key.pop(index)
                list_bag_and_key.insert(index, value)
            else:
                list_bag_and_key.insert(index, value)
        except KeyError:
            print("The bag '%s' or the key '%s' doesn't exist in the tab '%s'." % (bag, key, self.sheet_name))

    def display_value_by_bag_and_key(self, bag, key):
        print(self.get_value_by_bag_and_key(bag, key))

    def get_all_keys_by_bag(self, bag):
        try:
            return self.my_dict[bag].keys()
        except KeyError:
            print("The bag '%s' doesn't exist in the tab '%s'." % (bag, self.sheet_name))

    def get_all_keys(self):
        return self.my_dict2.keys()

    def get_value_by_key(self, key):
        try:
            return self.my_dict2[key]
        except KeyError:
            print("The key '%s' doesn't exist in the tab '%s'." % (key, self.sheet_name))

    def set_value_by_key(self, key, index, value):
        try:
            index -= 1
            list_of_values = self.my_dict2[key]
            if list_of_values:
                list_of_values.pop(index)
                list_of_values.insert(index, value)
            else:
                list_of_values.insert(index, value)
        except KeyError:
            print("The key '%s' doesn't exist in the tab '%s'." % (key, self.sheet_name))

    def is_key(self, key):
        keys_list = self.get_all_keys()
        if key in keys_list:
            return True
        else:
            return False

    @staticmethod
    def if_float_convert_to_int(cell):
        # Integer values in Excel are imported as floats in Python.
        # So we have to convert floats (2, 3) into integer
        if cell.ctype in (2, 3):
            return int(cell.value)
        else:
            return cell.value
