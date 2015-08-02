# -*-coding:UTF-8 -*


class ArrayParsing(object):
    """"
    This class is used to parse a sheet which contains an array.

    ..  note::
        By default, if the cell A1 doesn't contain the words 'List' or 'Text', then the sheet
        is considered as an Array.

    """
    # TODO description des méthodes

    def __init__(self, xl_sheet):
        self.xl_sheet = xl_sheet
        self.sheet_name = xl_sheet.name
        self.commands = self.get_all_commands()
        self.index = dict()

        # We check if there is duplications in the headers and indexes
        index_list = self.is_duplication(self.get_all_indexes())
        if index_list[0] is True:
            raise SystemExit("The index(es) in tab '%s' are duplicated: %s" % (self.sheet_name, index_list[1:]))

        header_list = self.is_duplication(self.get_all_headers())
        if header_list[0] is True:
            raise SystemExit("The parameter(s) in tab '%s' are duplicated: %s" % (self.sheet_name, header_list[1:]))

        # We parse the array to get the value of the cells
        for row_idx in range(1, xl_sheet.nrows):
            cell = xl_sheet.cell(row_idx, 0)
            if cell.ctype in (2, 3):
                cell_value = int(cell.value)
            else:
                cell_value = cell.value
            self.index[str(cell_value)] = dict()
            for col_idx in range(0, self.get_nbr_of_cols_in_row(0)):
                var_obj = xl_sheet.cell(row_idx, col_idx)
                if var_obj.ctype in (2, 3):
                    var_obj = int(var_obj.value)
                else:
                    var_obj = var_obj.value
                param_value = str(xl_sheet.cell(0, col_idx).value)

                self.index[str(cell_value)][param_value] = str(var_obj)

    def get_param_by_index(self, index_value, param_value):
        try:
            return self.index[index_value][param_value]
        except KeyError:
            print("The index '%s' or the parameter '%s' doesn't exist in the tab '%s'."
                  % (index_value, param_value, self.sheet_name))
            return KeyError

    def set_param_by_index(self, index_value, param_value, updated_value):
        try:
            self.index[index_value][param_value] = updated_value
        except KeyError:
            print("The index '%s' or the parameter '%s' doesn't exist in the tab '%s'."
                  % (index_value, param_value, self.sheet_name))

    def get_all_param_by_index(self, index_value):
        my_dict = dict()
        for param in self.get_all_headers():
            my_dict[str(param)] = self.get_param_by_index(index_value, param)
        return my_dict

    def display_param_by_index(self, index_value, param_value):
        print(self.get_param_by_index(index_value, param_value))

    def get_nbr_of_rows(self):
        """ This method returns the number of rows in the sheet.
        """
        return self.xl_sheet.nrows

    def get_nbr_of_cols(self):
        """ This method returns the number of columns in the sheet.
        """
        return self.xl_sheet.ncols

    def get_nbr_of_cols_in_row(self, row):
        """ This method returns the number of columns in the specified row.
        """
        return self.xl_sheet.row_len(row)

    def get_all_headers(self):
        """ This method get all the headers of the array.

        Returns:
            This method returns a list of headers.
        """
        headers = list()
        for col_idx in range(0, self.get_nbr_of_cols_in_row(0)):
            headers.append(str(self.xl_sheet.cell(0, col_idx).value))
        return headers

    def get_all_indexes(self):
        """ This method get all the indexes of the array.

        Returns:
            This method returns a list of indexes.
        """
        indexes = list()
        for row_idx in range(1, self.delimitation_between_indexes_and_commands()):
            cell = self.xl_sheet.cell(row_idx, 0)
            # If cell.ctype == xlrd.XL_CELL_NUMBER and xlrd.XL_CELL_DATE
            # because xlrd get a float number
            if cell.ctype in (2, 3):
                cell_value = int(cell.value)
            else:
                cell_value = cell.value
            indexes.append(str(cell_value))
        # Remove the empty value
        for iterator in range(0, indexes.count('')):
            indexes.remove('')
        return indexes

    def is_key_in_list(self, key, list):
        """ This method check if a given key is present is a list.

        Args:
            param key: the key
            param list: the list in which we have to looking for the key

        Returns:
            This method return 'True' if the key is present, 'False' otherwise.
        """
        if key in list:
            return True
        else:
            return False

    def is_duplication(self, key_list):
        """ This method controls if there is a duplicate header.

        Args:
            param key_list: list of item
            type key_list: list()

        Returns:
            An array. The first element is a boolean, if the value is 'True' then the list
            contains a duplicate item, 'False' otherwise.
            Finally, the array contains the duplicated items (if bool==true).
        """
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
        """ Get all the command templates. These templates are used to generate auto-formatted commands with the
         data contained into the array.

         Returns:
            A dictionary with the title of the commands as a key, and the commands associated.
        """
        commands = dict()
        command_row = self.get_row_where_value('Default')
        if command_row != -1:
            for row_idx in range(command_row, self.get_nbr_of_rows(), 2):
                cell = self.xl_sheet.cell(row_idx, 0)
                if cell.ctype in (2, 3):
                    cell_value = int(cell.value)
                else:
                    cell_value = cell.value
                if (cell_value != "" and (row_idx + 1) < self.get_nbr_of_rows()):
                    commands[cell_value] = str(self.xl_sheet.cell(row_idx + 1, 0).value)
                else:
                    commands[cell_value] = ""
            return commands

    def get_row_where_value(self, value):
        """ Get the number of the row where the value appears in the list of indexes.

        Args:
            param value: value of the index

        Returns:
            The number of the row, -1 otherwise
        """
        for row_idx in range(1, self.xl_sheet.nrows):
            cell = self.xl_sheet.cell(row_idx, 0)

            if cell.ctype in (2, 3):
                cell_value = int(cell.value)
            else:
                cell_value = cell.value

            if str(cell_value) == str(value):
                return row_idx
        return -1

    def delimitation_between_indexes_and_commands(self):
        if self.get_row_where_value('Default') == -1:
            return self.get_nbr_of_rows()
        else:
            return self.get_row_where_value('Default')