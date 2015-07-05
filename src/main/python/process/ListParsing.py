# -*-coding:UTF-8 -*

class ListParsing(object):
    # TODO Description of the class and its method
    global my_dict, my_dict2
    my_dict = dict()
    my_dict2 = dict()

    def __init__(self, xl_sheet):

        for row_idx in range(1, xl_sheet.nrows):
            self.xl_sheet = xl_sheet
            self.sheet_name = xl_sheet.name

            bag_cell = xl_sheet.cell(row_idx, 0)
            bag = str(self.if_float_convert_to_int(bag_cell))
            key_cell = xl_sheet.cell(row_idx, 1)
            key = str(self.if_float_convert_to_int(key_cell))
            value_cell = xl_sheet.cell(row_idx, 2)
            value = str(self.if_float_convert_to_int(value_cell))

            if not bag in my_dict.keys():
                my_dict[bag] = dict()

            my_dict2[key] = value
            my_dict[bag][key] = value

    def get_value_by_bag_and_key(self, bag, key):
        try:
            return my_dict[bag][key]
        except KeyError:
            print("The bag '%s' or the key '%s' doesn't exist in the tab '%s'." \
                  % (bag, key, self.sheet_name))

    def set_value_by_bag_and_key(self, bag, key, value):
        try:
            my_dict[bag][key] = value
        except KeyError:
            print("The bag '%s' or the key '%s' doesn't exist in the tab '%s'." \
                  % (bag, key, self.sheet_name))

    def display_value_by_bag_and_key(self, bag, key):
        print(self.get_value_by_bag_and_key(bag, key))

    def get_all_keys_by_bag(self, bag):
        try:
            return my_dict[bag].keys()
        except KeyError:
            print("The bag '%s' doesn't exist in the tab '%s'." % (bag, self.sheet_name))

    def get_all_keys(self):
        return my_dict2.keys()

    def get_value_by_key(self, key):
        try:
            return my_dict2[key]
        except KeyError:
            print("The key '%s' doesn't exist in the tab '%s'." % (key, self.sheet_name))

    def set_value_by_key(self, key, value):
        try:
            my_dict2[key] = value
        except KeyError:
            print("The key '%s' doesn't exist in the tab '%s'." % (key, self.sheet_name))

    def is_key(self, key):
        keys_list = self.get_all_keys()
        if key in keys_list:
            return True
        else:
            return False

    def if_float_convert_to_int(self, cell):
        # Integer values in Excel are imported as floats in Python.
        # So we have to convert floats (2, 3) into integer
        if cell.ctype in (2, 3):
            return int(cell.value)
        else:
            return cell.value