# -*-coding:UTF-8 -*

import re
from process.ArrayParsing import ArrayParsing
from process.TextParsing import TextParsing
from process.ListParsing import ListParsing


localVariableRegexp = '{{.*}}'
pattern_to_fill_regexp = '{{.*}}'
globalVariableRegexp = '\[\[.*\]\]'
unfilled_variable_counter = 1


def fill_out_the_template(template, workbook):
    pattern_to_fill = re.findall(pattern_to_fill_regexp, template)
    if pattern_to_fill:
        for pattern in pattern_to_fill:
            template = template.replace(pattern, get_value_of_pattern(remove_brackets(pattern), workbook))
    return template


def get_value_of_pattern(pattern, workbook):
    global unfilled_variable_counter
    splitPattern = re.split("[!,:]+", pattern)
    instanceOfSplitPattern = workbook[splitPattern[0]]
    print(instanceOfSplitPattern)
    if isinstance(instanceOfSplitPattern, ArrayParsing):
        result = workbook[splitPattern[0]].get_value_of_var_by_index_and_param(splitPattern[1], splitPattern[2])
        if result is KeyError:
            nbr_of_error = nbr_of_error + 1
            return "<unavailable to fill out>"
        else:
            return result
    elif isinstance(instanceOfSplitPattern, ListParsing):
        result = workbook[splitPattern[0]].get_value_by_bag_and_key_and_index(splitPattern[1], splitPattern[2],
                                                                              int(splitPattern[3]))
        if result is KeyError:
            nbr_of_error = nbr_of_error + 1
            return "<unavailable to fill out>"
        else:
            return result
    elif isinstance(instanceOfSplitPattern, TextParsing):
        result = workbook[splitPattern[0]].get_text_by_title(splitPattern[1])
        if result is KeyError:
            nbr_of_error = nbr_of_error + 1
            return "<unavailable to fill out>"
        else:
            return result
    else:
        nbr_of_error = nbr_of_error + 1
        return "<unavailable to fill out>"

def fill_out(my_string, tab, index, dict):
    isLocalVar = re.findall(localVariableRegexp, my_string)
    if isLocalVar:
        for var in isLocalVar:
            my_string = my_string.replace(var, get_value(remove_brackets(var)))
    return my_string

def get_value(var, tab, index, dict):
    is_brackets = re.findall(localVariableRegexp, var)
    if is_brackets:
        test = var.replace(is_brackets[0], get_value(remove_brackets(is_brackets[0]), tab, index, dict))
        if test[0] == '$':
            return str(tab['Global'].get_value_of_var_by_index_and_param(index, test[1:]))
        elif re.search('!', test):
            # We split the "Sheet![Index,Parameter] in a list of [Sheet, Index, Parameter]
            test = re.split('\W+', test)
            return str(tab[test[0]].get_value_of_var_by_index_and_param(test[1], test[2]))
        else:
            return str(dict[test])
    else:
        if var[0] == '$':
            return str(tab['Global'].get_value_of_var_by_index_and_param(index, var[1:]))
        elif re.search('!', var):
            # We split the "Sheet![Index,Parameter] in a list of [Sheet, Index, Parameter]
            var = re.split('\W+', var)
            return str(tab[var[0]].get_value_of_var_by_index_and_param(var[1], var[2]))
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
