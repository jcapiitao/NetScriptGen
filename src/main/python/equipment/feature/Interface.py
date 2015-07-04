from process.ArrayParsing import ArrayParsing

FUNCTION = 'Function'
EQUIPMENT = 'Equipment'
TYPE_OF_INTERFACE = 'TypeOfInterface'
SLOT = 'Slot'
SUBLSLOT = 'Subslot'
INTERFACES = 'Interfaces'


class Interface(ArrayParsing):
    """ This class provides methods to deal with interfaces of an equipemnt.
    """

    def __init__(self, xl_sheet):
        super().__init__(xl_sheet)

    def get_by_equipment_and_function(self, equipment, function):
        """ This method gets the interfaces which are used for a typical function (data, voice, wifi, printer, and so on)
        within an equipment.

        Args:
            param equipment: the network equipment we want to get the interfaces
            param function: the function of the interfaces

        Returns:
            This methode returns a list as follows ['TYPE_OF_INTERFACE', 'SLOT', 'SUBLSLOT', 'INTERFACES']
            example: ['Gigabit', '1', '0', '1']
        """
        myList = list()
        for row in range(1, self.delimitation_between_indexes_and_commands()):
            equip = self.get_param_by_index(str(row), EQUIPMENT)
            func = self.get_param_by_index(str(row), FUNCTION)
            if equip == equipment and func == function:
                for item in (TYPE_OF_INTERFACE, SLOT, SUBLSLOT, INTERFACES):
                    myList.append(self.get_param_by_index(str(row), item))
        return myList

    def get_by_equipment_and_function_in_stack(self, equipment, function, stack=1):
        """ This method gets the interfaces which are used for a typical function (data, voice, wifi, printer, and so on)
        within an equipment. Furthermore, if the equipments are stacked, we get all the interfaces of the stack.

        Args:
            param equipment: the network equipment we want to get the interfaces
            param function: the function of the interfaces
            param stack: the number of equipments being stacked (stack = 1 by default)

        Returns:
            This method returns a string as follows 'Gigabit 1/0/1-2,Gigabit 2/0/1-2,Gigabit 3/0/1-2'
        """
        interfaces = self.get_by_equipment_and_function(equipment, function)
        allInterfaces = list()
        for i in range(int(interfaces[1]), stack+1):
            interfaces[1] = str(i)
            allInterfaces.append(self.in_string(interfaces))
        return ','.join(allInterfaces)

    def in_string(self, list):
        """ This method formats a list in a string

         Args:
            param list: the list which contains informations about the interfaces

         Returns:
            This method returns 'Gigabit 1/0/1' for example
        """
        return list[0] + ' ' + '/'.join(list[1:])








