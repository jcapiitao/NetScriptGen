# -*-coding:UTF-8 -*


class ListParsing(object):
    # TODO Description of the class

    def __init__(self, xl_sheet):
        self.xl_sheet = xl_sheet
        self.sheet_name = xl_sheet.name
        self.dict_bags_and_keys = dict()
        self.dict_only_keys = dict()
        for row_idx in range(1, xl_sheet.nrows):
            list_of_values = list()
            bag_obj = xl_sheet.cell(row_idx, 0)
            bag_value = self.to_string(bag_obj)
            key_obj = xl_sheet.cell(row_idx, 1)
            key_value = self.to_string(key_obj)
            col_idx = 2
            while col_idx < xl_sheet.ncols:
                if xl_sheet.cell(row_idx, col_idx).ctype not in (0, 6):
                    value_obj = xl_sheet.cell(row_idx, col_idx)
                    list_of_values.append(self.to_string(value_obj))
                col_idx += 1
            if bag_value not in self.dict_bags_and_keys.keys():
                self.dict_bags_and_keys[bag_value] = dict()
            self.dict_only_keys[key_value] = list_of_values
            self.dict_bags_and_keys[bag_value][key_value] = list_of_values

    def get_value_by_bag_and_key(self, bag, key):
        try:
            return self.dict_bags_and_keys[bag][key]
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
            list_bag_and_key = self.dict_bags_and_keys[bag][key]
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
            return self.dict_bags_and_keys[bag].keys()
        except KeyError:
            print("The bag '%s' doesn't exist in the tab '%s'." % (bag, self.sheet_name))

    def get_all_keys(self):
        return self.dict_only_keys.keys()

    def get_value_by_key(self, key):
        try:
            return self.dict_only_keys[key]
        except KeyError:
            print("The key '%s' doesn't exist in the tab '%s'." % (key, self.sheet_name))

    def set_value_by_key(self, key, index, value):
        try:
            index -= 1
            list_of_values = self.dict_only_keys[key]
            if list_of_values:
                list_of_values.pop(index)
                list_of_values.insert(index, value)
            else:
                list_of_values.insert(index, value)
        except KeyError:
            print("The key '%s' doesn't exist in the tab '%s'." % (key, self.sheet_name))

    @staticmethod
    def to_string(cell_obj):
        # Integer values in Excel are imported as floats in Python.
        # So we have to convert floats (2, 3) into integer
        if cell_obj.ctype in (2, 3):
            cell_value = int(cell_obj.value)
            return str(cell_value)
        else:
            return cell_obj.value
