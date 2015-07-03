#!/usr/bin/python3
# -*-coding:UTF-8 -*

import xlrd
from utils.files import get_full_path

# TODO : Transformer la fonction en classe et implémenter le DP Singleton


path = get_full_path('test.xlsx')

def getExcelFile():
    return path

def getExcelWorkbook():
    return xlrd.open_workbook(path)

def getSheet(sheet_name):
    wb = getExcelWorkbook()
    return wb.sheet_by_name(sheet_name)