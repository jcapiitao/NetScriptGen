# -*-coding:UTF-8 -*


class TextParsing(object):

    def __init__(self, xl_sheet):
        self.dict_of_texts = dict()
        self.xl_sheet = xl_sheet
        self.sheet_name = xl_sheet.name
        for row_idx in range(1, self.xl_sheet.nrows):
            title_obj = self.xl_sheet.cell(row_idx, 0)
            title_value = self.to_string(title_obj)
            text_obj = self.xl_sheet.cell(row_idx, 1)
            text_value = self.to_string(text_obj)
            self.dict_of_texts[title_value] = text_value

    def get_text_by_title(self, title):
        try:
            return self.dict_of_texts[title]
        except KeyError:
            print("The title '%s' doesn't exist in the tab '%s'." % (title, self.sheet_name))

    def set_text_by_title(self, title, text):
        try:
            self.dict_of_texts[title] = text
        except KeyError:
            print("The title '%s' doesn't exist in the tab '%s'." % (title, self.sheet_name))

    def display_text_by_title(self, title):
        print(self.get_text_by_title(title))

    def get_all_titles(self):
        list_of_titles = list()
        for row_idx in range(1, self.xl_sheet.nrows):
            title_obj = self.xl_sheet.cell(row_idx, 0)
            title_value = self.to_string(title_obj)
            if title_value != '':
                list_of_titles.append(title_value)
        return list_of_titles

    def is_title(self, title):
        title_list = self.get_all_titles()
        if title in title_list:
            return True
        else:
            return False

    @staticmethod
    def to_string(cell_obj):
        # Integer values in Excel are imported as floats in Python.
        # So we have to convert floats (2, 3) into integer
        if cell_obj.ctype in (2, 3):
            cell_value = int(cell_obj.value)
            return str(cell_value)
        else:
            return cell_obj.value
