# -*-coding:UTF-8 -*

import os
import sys
import xlrd

MAIN_DIRECTORY = os.path.dirname(os.path.dirname(__file__))


def get_full_path(*path):
    return os.path.join(MAIN_DIRECTORY, *path)


def get_test_file(file):
    main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    excel_file_path = os.path.join(main_path, 'unittest', 'excel_file')
    return os.path.join(excel_file_path, file)


def open_file(file):
    try:
        if os.path.isfile(file):
            return open(file, 'r', -1, 'UTF-8').read()
        else:
            print("The file '%s' doesn't exist" % file)
            sys.exit(1)
    except OSError:
        print('Unable to open the file : %s' % file)
        sys.exit(1)


def get_test_excel_file():
    return get_test_file('test.xlsx')


def get_excel_workbook(file=get_test_excel_file()):
    return xlrd.open_workbook(file)


def get_sheet(sheet_name):
    wb = get_excel_workbook()
    return wb.sheet_by_name(sheet_name)


def get_sheet_test(file, sheet_name="Sheet1"):
    file = get_test_file(file)
    wb = get_excel_workbook(file)
    return wb.sheet_by_name(sheet_name)
