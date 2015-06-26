from process.ArrayParsing import ArrayParsing

FUNCTION = 'Function'
EQUIPMENT = 'Equipment'
INTERFACES = 'Interfaces'
SUBLSLOT = 'Sublslot'
SLOT = 'Slot'
TYPE_OF_INTERFACE = 'TypeOfInterface'


class Interface(ArrayParsing):

    def __init__(self, xl_sheet):
        super().__init__(xl_sheet)
        Interface.nbrOfRows = ArrayParsing.get_nbr_of_rows(self)

    def get_by_function(self, equipment, function):
        myList = list()
        for i in range(1, self.nbrOfRows):
            if ArrayParsing.get_param_by_index(i, EQUIPMENT) is equipment and ArrayParsing.get_param_by_index(i, FUNCTION) is function:
                for item in range(TYPE_OF_INTERFACE, SLOT, SUBLSLOT, INTERFACES):
                    myList.append(self.get_param_by_index(i, item))
                return myList

    def get_by_function_and_stack(self, equipment, function, stack):
        interfaces = self.get_by_function(self, equipment, function)
        allInterfaces = list()
        for i in range(interfaces[1], stack):
            interfaces[1] = i
            allInterfaces.append(self.in_string(interfaces))
        return ','.join(allInterfaces)

    def in_string(self, list):
        return list[0] + ' ' + '/'.join(list[1:])








