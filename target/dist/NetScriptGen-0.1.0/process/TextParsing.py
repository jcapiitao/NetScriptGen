# -*-coding:UTF-8 -*


class TextParsing(object):

    def __init__(self, xl_sheet):
        self.my_dict = dict()
        self.xl_sheet = xl_sheet
        self.sheet_name = xl_sheet.name
        for row_idx in range(1, self.xl_sheet.nrows):
            self.my_dict[self.xl_sheet.cell(row_idx, 0).value] = self.xl_sheet.cell(row_idx, 1).value

    def get_text_by_title(self, title):
        try:
            return self.my_dict[title]
        except KeyError:
            print("The title '%s' doesn't exist in the tab '%s'." % (title, self.sheet_name))

    def set_text_by_title(self, title, text):
        try:
            self.my_dict[title] = text
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
