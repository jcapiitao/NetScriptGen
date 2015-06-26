#!/usr/bin/python3
# -*-coding:UTF-8 -*


import xlrd


class ExtractExcelData(object):
    def __init__(self, wb):

        self.wb = wb
        sheet_names = wb.sheet_names()

        for sheet in sheet_names:
            xl_sheet = wb.sheet_by_name(sheet)
            if xl_sheet.cell(0, 0).value == 'List':
                test = ListParsing(xl_sheet)
            print(sheet)

        return


"""
fname = "C:/Users/joec/Desktop/joware/joware-v2/test.xlsx"
wb = xlrd.open_workbook(fname)

book = ExtractExcelData(wb)
"""
