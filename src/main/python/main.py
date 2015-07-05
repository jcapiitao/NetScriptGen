# -*-coding:UTF-8 -*

# TODO : Use Sphinx for doc generation

import os
from process.ArrayParsing import ArrayParsing
from process.TextParsing import TextParsing
from process.ListParsing import ListParsing
from function.ReplaceValue import fill_out
from equipment.feature.Vlan import Vlan
from equipment.feature.Interface import Interface
from utils.ExcelFile import getExcelWorkbook
from utils.files import get_full_path


wb = getExcelWorkbook()
global_template_file = get_full_path('ios_script_sample2.txt')
sheet_names = wb.sheet_names()
tab = dict()

try:
    if os.path.isfile(global_template_file):
        template = open(global_template_file, 'r', -1,' UTF-8')
    else:
        raise SystemExit("The file '%s' doesn't exit" % global_template_file)
except OSError:
    raise SystemExit('Unable to open the global template')


for sheet in sheet_names:
    xl_sheet = wb.sheet_by_name(sheet)
    if (xl_sheet.cell(0, 0).value == 'Function' and
                xl_sheet.cell(0, 1).value == 'Variable' and
                xl_sheet.cell(0, 2).value == 'Value'):
        tab[sheet] = ListParsing(xl_sheet)
    elif xl_sheet.cell(0, 0).value == 'Text':
        tab[sheet] = TextParsing(xl_sheet)
    elif sheet == 'Interfaces':
        tab[sheet] = Interface(xl_sheet)
    else:
        print(xl_sheet.name)
        tab[sheet] = ArrayParsing(xl_sheet)


index = 'HOST1'
informations = tab['Global'].get_param_by_index(index)
script = fill_out(template, tab, index, informations)
print(script)

'''
feature = "VTP_Profile"
index = 'HOST1'
my_feature_value = tab['Global'].get_param_by_index(index, feature)


vlans = Vlan(tab)
print(vlans.get_functions())
print(vlans.get_vlan_IDs_by_function_with_delimiter("Trunk", index, tab, ','))
print(vlans.get_vlan_names())
if my_feature_value != "":
    my_dict = tab[feature].get_all_param_by_index(my_feature_value)
    my_commands = tab[feature].get_all_commands()
    sub_template = my_commands[tab[feature].get_param_by_index(my_feature_value, "Template")]
    script = fill_out(sub_template, tab, index, my_dict)
    print(script)



test = tab['Global variable'].get_all_keys()
test.insert(2, 'test')
print(test)

print(tab['VLAN'].is_key_in_list('24', tab['VLAN'].get_all_indexes()))
print(tab['VLAN'].get_param_by_index('101', 'Mask'))
tab['VTP_Profile'].display_param_by_index('VTP_Profile2', 'VTP_MODE')
tab['VTP_Profile'].set_param_by_index('VTP_Profile2', 'VTP_MODE', '0.0.0.0')
tab['VTP_Profile'].display_param_by_index('VTP_Profile2', 'VTP_MODE')
print(tab['VLAN'].get_param_by_index('22', 'Name'))

tab['Global variable'].display_value_by_bag_and_key('DNS', 'DNS Server 1')
tab['Global variable'].display_value_by_bag_and_key('DNS', 'DNS Server')
tab['Interfaces'].display_value_by_bag_and_key('CISCO WS-C3750v2-48PS-S', 'Uplink')
'''