# -*-coding:UTF-8 -*

import xlrd


class TextParsing(object):
    # TODO Description of the class and its method
    global my_dict
    my_dict = dict()

    def __init__(self, xl_sheet):

        for row_idx in range(1, xl_sheet.nrows):
            self.xl_sheet = xl_sheet
            self.sheet_name = xl_sheet.name

            my_dict[xl_sheet.cell(row_idx, 0).value] = xl_sheet.cell(row_idx, 1).value

    def get_text_by_title(self, title):
        try:
            return my_dict[title]
        except KeyError:
            print("The title '%s' doesn't exist in the tab '%s'." % (title, self.sheet_name))

    def set_text_by_title(self, title, text):
        try:
            my_dict[title] = text
        except KeyError:
            print("The title '%s' doesn't exist in the tab '%s'." % (title, self.sheet_name))


    def display_text_by_title(self, title):
        print(self.get_text_by_title(title))

    def get_all_titles(self):
        keys_list = list()
        for row_idx in range(1, self.xl_sheet.nrows):
            title = self.xl_sheet.cell(row_idx, 0).value
            if title != '':
                keys_list.append(title)
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
