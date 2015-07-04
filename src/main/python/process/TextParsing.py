# -*-coding:UTF-8 -*

import xlrd


class TextParsing(object):
    global my_dict
    my_dict = dict()

    def __init__(self, xl_sheet):

        for row_idx in range(1, xl_sheet.nrows):
            self.xl_sheet = xl_sheet

            my_dict[xl_sheet.cell(row_idx, 0).value] = xl_sheet.cell(row_idx, 1).value

    def get_text_by_title(self, title):
        return my_dict[title]

    def set_text_by_title(self, title, text):
        my_dict[title] = text

    def display_text_by_title(self, title):
        print(self.get_text_by_title(title))

    def get_all_titles(self):
        keys_list = list()
        for row_idx in range(1, self.xl_sheet.nrows):
            keys_list.append(self.xl_sheet.cell(row_idx, 0).value)
        return keys_list

    def is_title(self, title):
        title_list = self.get_all_titles()
        if title in title_list:
            return True
        else:
            return False


"""
fname = "C:/Users/joec/Desktop/joware/joware-v2/test.xlsx"
wb = xlrd.open_workbook(fname)
my_sheet = wb.sheet_by_name('Text')

text = TextParsing(my_sheet)
print(text.is_title('banner'))
text.display_text_by_title('banner')
print(text.get_all_titles())
text.display_text_by_title('test')
"""
