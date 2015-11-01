# -*-coding:UTF-8 -*

# TODO : Use Sphinx for doc generation

import getopt
from process.ArrayParsing import ArrayParsing
from process.TextParsing import TextParsing
from process.ListParsing import ListParsing
from equipment.Equipment import Equipment
from equipment.feature.Interface import Interface
from utils.ExcelWorkbookManager import *


def main(excel_file, template_file, directory):
    wb = get_excel_workbook(excel_file)
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

    if not directory:
        directory = os.path.dirname(template_file)
    is_directory = False
    version_number = 1
    while is_directory is False:
        directory_name = ''.join(['scripts-', os.path.splitext(os.path.basename(excel_file))[0], '-v',
                                  str(version_number)])
        if os.path.isdir(os.path.join(directory, directory_name)) is False:
            directory = os.path.join(directory, directory_name)
            os.mkdir(directory)
            is_directory = True
        version_number += 1
    list_of_equipments = list()
    for hostname in workbook['Global'].get_all_indexes():
        equipment = Equipment(hostname, template, workbook)
        list_of_equipments.append(equipment)
        equipment.save_script_as(directory, hostname)

if __name__ == "__main__":
    argv = sys.argv
    excel_file, template_file, directory = '', '', ''
    if not argv[1:]:
        print('netscriptgen -e <excelFile> -t <scriptTemplate> -o <directory>')
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv[1:], "h:e:t:o:", ["excelFile=", "scriptTemplate=", "directory"])
    except getopt.GetoptError:
        print('netscriptgen -e <excelFile> -t <scriptTemplate> -o <directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('netscriptgen -e <excelFile> -t <scriptTemplate> -o <directory')
            sys.exit()
        elif opt in ("-e", "--excelFile"):
            excel_file = arg
        elif opt in ("-t", "--scriptTemplate"):
            template_file = arg
        elif opt in ("-o", "--directory"):
            directory = arg
    if not excel_file or template_file:
        print('netscriptgen -e <excelFile> -t <scriptTemplate> -o <directory>')
        sys.exit(2)

    main(excel_file, template_file, directory)
