# -*-coding:UTF-8 -*

# TODO : Use Sphinx for doc generation

from process.ArrayParsing import ArrayParsing
from process.TextParsing import TextParsing
from process.ListParsing import ListParsing
from function.ReplaceValue import fill_out
from equipment.feature.Vlan import Vlan
from equipment.feature.Interface import Interface
import xlrd


fname = "/home/joel/ownCloud/Developpement/NetScriptGen/test.xlsx"
#fname = r'D:\ownCloud\Developpement\NetScriptGen\test.xlsx'
wb = xlrd.open_workbook(fname)
sheet_names = wb.sheet_names()
tab = dict()

for sheet in sheet_names:
    xl_sheet = wb.sheet_by_name(sheet)

    if (xl_sheet.cell(0, 0).value == 'Function' and xl_sheet.cell(0, 1).value == 'Variable' and xl_sheet.cell(0, 2).value == 'Value'):
        tab[sheet] = ListParsing(xl_sheet)
    elif xl_sheet.cell(0, 0).value == 'Text':
        tab[sheet] = TextParsing(xl_sheet)
    elif sheet == 'Interfaces':
        tab[sheet] = Interface(xl_sheet)
    else:
        #print(sheet)
        tab[sheet] = ArrayParsing(xl_sheet)



feature = "VTP_Profile"
index = 'HOST1'
my_feature_value = tab['Global'].get_param_by_index(index, feature)


print(Interface.get_by_function_and_stack(Interface, 'CISCO WS-C3750v2-48PS-S', 'Uplink', '5'))
'''
vlans = Vlan(tab)
print(vlans.get_functions())
print(vlans.get_vlan_IDs_by_function_with_delimiter("Trunk", index, tab, ','))
print(vlans.get_vlan_names())
'''

if my_feature_value != "":
    my_dict = tab[feature].get_all_param_by_index(my_feature_value)
    my_commands = tab[feature].get_all_commands()
    sub_template = my_commands[tab[feature].get_param_by_index(my_feature_value, "Template")]
    script = fill_out(sub_template, tab, index, my_dict)
    print(script)
'''
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