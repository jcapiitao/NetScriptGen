#!/usr/bin/python3
# -*-coding:UTF-8 -*

import re
import string


localVariableRegexp = '{{.*}}'
globalVariableRegexp = '\[\[.*\]\]'

def fill_out(my_string, tab, index, dict):
    isLocalVar = re.findall(localVariableRegexp, my_string)
    if isLocalVar:
        for var in isLocalVar:
            my_string = my_string.replace(var, get_value(remove_brackets(var), tab, index, dict))
    return my_string

def get_value(var, tab, index, dict):
    is_brackets = re.findall(localVariableRegexp, var)
    if is_brackets:
        test = var.replace(is_brackets[0], get_value(remove_brackets(is_brackets[0]), tab, index, dict))
        if test[0] == '$':
            return str(tab['Global'].get_param_by_index(index, test[1:]))
        elif re.search('!', test):
            # We split the "Sheet![Index,Parameter] in a list of [Sheet, Index, Parameter]
            test = re.split('\W+', test)
            return str(tab[test[0]].get_param_by_index(test[1], test[2]))
        else:
            return str(dict[test])
    else:
        if var[0] == '$':
            return str(tab['Global'].get_param_by_index(index, var[1:]))
        elif re.search('!', var):
            # We split the "Sheet![Index,Parameter] in a list of [Sheet, Index, Parameter]
            var = re.split('\W+', var)
            return str(tab[var[0]].get_param_by_index(var[1], var[2]))
        else:
            # We fist search in local variables
            if var in dict and dict[var] != "":
                return str(dict[var])
            # If there is no match in local variables, then we try to find out a match with global variable
            elif tab['Global variable'].is_key(var):
                return tab['Global variable'].get_value_by_key(var)
            # If there is no match...
            else:
                return "None"

def remove_brackets(string):
    return string[2:-2]
