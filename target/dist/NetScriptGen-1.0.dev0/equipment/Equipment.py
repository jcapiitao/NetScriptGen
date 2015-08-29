# -*-coding:UTF-8 -*

import re
from process.ArrayParsing import ArrayParsing
from process.TextParsing import TextParsing
from process.ListParsing import ListParsing

class Equipment(object):
    #localVariableRegexp = '{{.*}}'
    #globalVariableRegexp = '\[\[.*\]\]'

    def __init__(self, hostname, template, workbook):
        self.hostname = hostname
        self.template = template
        self.workbook = workbook
        self.unfilled_variable_counter = 0
        self.pattern_contains_brackets = '{{.*}}'
        self.pattern_contains_exclamation_and_colon = '[!,:]'

    def get_script(self):
        script = self.fill_out_the_template()
        if self.unfilled_variable_counter != 0:
            line = "! /!\----- Warning : There is %s unfilled variable -----/!\\\n" % self.unfilled_variable_counter
            script = line + script
        return script

    def fill_out_the_template(self):
        pattern_to_fill = re.findall(self.pattern_contains_brackets, self.template)
        template = self.template
        if pattern_to_fill:
            for pattern in pattern_to_fill:
                template = template.replace(pattern, self.get_value_of_pattern(pattern, self.workbook))
        return template

    def save_script_as(self, path_of_the_folder, file_name):
        extension = '.txt'
        with open(path_of_the_folder + '/' + file_name + extension, "w") as file:
            file.write(self.get_script())
        file.close()

    def get_value_of_pattern(self, pattern, workbook):
        match_brackets = re.findall(self.pattern_contains_brackets, pattern)
        if match_brackets:
            for match in match_brackets:
                if re.findall(self.pattern_contains_exclamation_and_colon, match):
                    return self.get_value_pattern_with_exclamation_and_colon(match, workbook)
                else:
                    return self.get_value_from_global_sheet(match)


    def get_value_from_global_sheet(self, parameter):
        # If the parameter is a title of a sheet, we need to get data from this sheet
        parameter = self.remove_brackets(parameter)
        if parameter in self.workbook.keys():
            print("The parameter '%s 'is title of a sheet" %parameter)
            index = self.workbook['Global'].get_value_of_var_by_index_and_param(self.hostname, parameter)
            data_of_the_index = self.workbook[parameter].get_all_param_by_index(index)
            local_templates = self.workbook[parameter].get_local_templates()
            local_template = local_templates[self.workbook[parameter].get_value_of_var_by_index_and_param(index, "Template")]
            return self.fill_local_template(data_of_the_index, local_template)
        else:
            return self.workbook['Global'].get_value_of_var_by_index_and_param(self.hostname, parameter)

    def fill_local_template(self, data, local_template):
        is_brackets = re.findall(self.pattern_contains_brackets, local_template)
        if is_brackets:
            for value in is_brackets:
                local_template = local_template.replace(value, data[self.remove_brackets(value)])
        return local_template


    def get_value_pattern_with_exclamation_and_colon(self, pattern, workbook):
        pattern = self.remove_brackets(pattern)
        is_brackets = re.findall(self.pattern_contains_brackets, pattern)
        if is_brackets:
            for pattern_with_backets in is_brackets:
                value = self.get_value_pattern_with_exclamation_and_colon(pattern_with_backets, workbook)
                pattern = re.sub(self.pattern_contains_brackets, value, pattern)
        splitPattern = re.split("[!,:]+", pattern)
        instanceOfSplitPattern = workbook[splitPattern[0]]
        if isinstance(instanceOfSplitPattern, ArrayParsing):
            result = workbook[splitPattern[0]].get_value_of_var_by_index_and_param(splitPattern[1], splitPattern[2])
            if result is None:
                self.unfilled_variable_counter = self.unfilled_variable_counter + 1
                return "<unavailable to fill out>"
            else:
                return result
        elif isinstance(instanceOfSplitPattern, ListParsing):
            result = workbook[splitPattern[0]].get_value_by_bag_and_key_and_index(splitPattern[1], splitPattern[2],
                                                                                  int(splitPattern[3]))
            if result is None:
                self.unfilled_variable_counter = self.unfilled_variable_counter + 1
                return "<unavailable to fill out>"
            else:
                return result
        elif isinstance(instanceOfSplitPattern, TextParsing):
            result = workbook[splitPattern[0]].get_text_by_title(splitPattern[1])
            if result is None:
                self.unfilled_variable_counter = self.unfilled_variable_counter + 1
                return "<unavailable to fill out>"
            else:
                return result
        else:
            self.unfilled_variable_counter = self.unfilled_variable_counter + 1
            return "<unavailable to fill out>"


    def remove_brackets(self, string):
        return string[2:-2]

    def get_unfilled_variable_counter(self):
        return int(self.unfilled_variable_counter)

