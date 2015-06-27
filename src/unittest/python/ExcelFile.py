#!/usr/bin/python3
# -*-coding:UTF-8 -*

import xlrd
from utils.files import get_full_path

# TODO : Transformer la fonction en classe et implémenter le DP Singleton


path = get_full_path('test.xlsx')

def getExcelFile():
    return path

def getExcelWorbook():
    wb = xlrd.open_workbook(path)
    my_sheet = wb.sheet_by_name('VLAN')
    self.sheet = ArrayParsing(my_sheet)

def getSheet(sheet_name):
    wb = xlrd.open_workbook(path)
    return wb.sheet_by_name(sheet_name)