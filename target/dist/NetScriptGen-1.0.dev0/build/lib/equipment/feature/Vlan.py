import inspect
import logging
import re

class Vlan(object):

    vlanRegex = 'VLAN#'

    listOfVlans = list()
    functions = list()
    functions2 = dict()
    headers = list()


    def __init__(self, tab):
        self.tab = tab
        self.headers = tab['Global'].get_all_headers()

        # We try to find out if there are VLANs and if so, get their name in a list
        for header in self.headers:
            if re.findall(self.vlanRegex, header):
                self.listOfVlans.append(header)

        # If there is not at least one VLAN, we stop the processus and we return an empty object
        if len(self.listOfVlans) is 0:
            logging.info('There is not VLANs into this project')
            return None

        # Now we get the functions, we loop between the first and second Vlan
        for column in range(self.headers.index(self.listOfVlans[0]) + 1, self.headers.index(self.listOfVlans[1])):
            self.functions.append(self.headers[column])

        firstCol = int(self.headers.index(self.listOfVlans[0]))
        nbrOfFunctions = int(len(self.functions))
        nbrOfVlans = int(len(self.listOfVlans))
        lastCol = firstCol + ((nbrOfFunctions + 1) * (nbrOfVlans - 1))
        functionIterator = 1
        for function in self.functions:
            my_list = list()
            for i in range((firstCol + functionIterator), (lastCol + functionIterator), (nbrOfFunctions + 1)):
                my_list.append(self.headers[i])
            functionIterator = functionIterator + 1
            self.functions2[function] = my_list

        # We check if each VLAN has the same number of columns (function) on its right
        # VLAN1, Function1, Function 2, VLAN2, Function1, VLAN3, Function1, Function2--> NOT Good
        # VLAN1, Function1, Function 2, VLAN2, Function1, Function2, VLAN3, Function1, Function2 --> Good
        for function in self.functions:
            for f in self.functions2[function]:
                if re.findall(function, f) is False:
                    logging.error("Sheet 'Global': Each VLAN must have the same number of column corresponding to a function")

    def get_vlan_names(self):
        vlanNames = list()
        for vlan in self.listOfVlans:
            m = re.match(self.vlanRegex+"(\w+)", vlan)
            vlanNames.append(m.group(1))
        return vlanNames

    def get_vlan_IDs_by_function(self, function, index, tab):
        vlans = list()
        offset = self.functions.index(function) + 1
        for column in self.functions2[function]:
            vlanID = self.headers.index(column) - offset
            vlanName = self.headers[vlanID]
            var = tab['Global'].get_param_by_index(index, column)
            if var == "YES":
                vlans.append(str(tab['Global'].get_param_by_index(index, vlanName)))
        return vlans

    def get_vlan_IDs_by_function_with_delimiter(self, function, index, tab, delimiter = ','):
        vlans = self.get_vlan_IDs_by_function(function, index, tab)
        print(vlans)
        return str.join(delimiter, vlans)

    def get_functions(self):
        return self.functions2







