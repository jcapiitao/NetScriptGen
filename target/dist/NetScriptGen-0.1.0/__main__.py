# -*-coding:UTF-8 -*

# TODO : Use Sphinx for doc generation

import sys
import getopt
import io
from process.ArrayParsing import ArrayParsing
from process.TextParsing import TextParsing
from process.ListParsing import ListParsing
from equipment.Equipment import Equipment
from function.ReplaceValue import *
from equipment.feature.Vlan import Vlan
from equipment.feature.Interface import Interface
from utils.ExcelWorkbookManager import *


def main(argv=None):
    excel_file = get_full_path('test.xlsx')
    template_file = get_full_path('ios_script_sample2.txt')
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:],"h:e:t:o:",["excelFile=","scriptTemplate=","log"])
    except getopt.GetoptError:
        print('netScriptGen.py -e <excelFile> -t <scriptTemplate> -o <log>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('netScriptGen.py -e <excelFile> -t <scriptTemplate> -o <log>')
            sys.exit()
        elif opt in ("-e", "--excelFile"):
            excel_file = arg
        elif opt in ("-t", "--scriptTemplate"):
            template_file = arg

    wb = get_excel_workbook(excel_file)
    # wb = get_excel_workbook()
    # template_file = get_full_path('ios_script_sample2.txt')
    sheet_names = wb.sheet_names()
    workbook = dict()
    template = open_file(template_file)

    for sheet in sheet_names:
        xl_sheet = wb.sheet_by_name(sheet)
        if (xl_sheet.cell(0, 0).value == 'Function' and
                xl_sheet.cell(0, 1).value == 'Variable' and
                xl_sheet.cell(0, 2).value == 'Value'):
            workbook[sheet] = ListParsing(xl_sheet)
        elif xl_sheet.cell(0, 0).value == 'Text':
            workbook[sheet] = TextParsing(xl_sheet)
        elif sheet == 'Interfaces':
            workbook[sheet] = Interface(xl_sheet)
        else:
            workbook[sheet] = ArrayParsing(xl_sheet)

    # Now we fill out the template

    list_of_equipments = list()
    # for hostname in workbook['Global'].get_all_indexes():
    hostname = 'HOST1'
    equipment = Equipment(hostname, template, workbook)
    list_of_equipments.append(equipment)
    print("-------------- Script Output --------------")
    print(equipment.get_script())
    # quipment.save_script_as(get_full_path(), hostname)
    # print("There is %s unfilled variable " % equipment.get_unfilled_variable_counter())

if __name__ == "__main__":
    main()
