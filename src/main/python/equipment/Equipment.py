# -*-coding:UTF-8 -*

import re
import sys
from process.ArrayParsing import ArrayParsing
from process.TextParsing import TextParsing
from process.ListParsing import ListParsing


class Equipment(object):

    def __init__(self, hostname, template, workbook):
        self.hostname = hostname
        self.template = template
        self.workbook = workbook
        self.unresolved = 0
        self.pattern_contains_braces = '(?<=\{\{).+?(?=\}\})'
        self.pattern_contains_brackets = '\(\((.*)\)\)'
        self.pattern_contains_interrogation = '[?]'
        self.pattern_contains_exclamation_and_colon = '[!,:]'

    def get_script(self):
        script = self.fill_out_the_template()
        if self.unresolved != 0:
            line = "! ----- Warning : There is %s unresolved variable -----\n" % self.unresolved
            script = line + script
        return script

    def fill_out_the_template(self):
        var_to_fill = re.findall(self.pattern_contains_braces, self.template)
        template = self.template
        if var_to_fill:
            for var in var_to_fill:
                template = template.replace(''.join(['{{', var, '}}']),
                                            self.get_value_of_var(var, self.workbook))
            return template
        else:
            print('There is not variable to fill out')
            sys.exit()

    def save_script_as(self, path_of_the_folder, file_name):
        extension = '.txt'
        with open(path_of_the_folder + '/' + file_name + extension, "w") as file:
            file.write(self.get_script())
        file.close()

    def get_value_of_var(self, var, workbook):
        if re.findall(self.pattern_contains_exclamation_and_colon, var):
            return self.get_value_of_var_with_exclamation_and_colon(var, workbook)
        elif re.findall(self.pattern_contains_interrogation, var):
            return self.get_value_of_var_with_interrogation(var, workbook)
        else:
            return self.get_value_of_var_from_global_sheet(var)

    def get_value_of_var_from_global_sheet(self, parameter):
        # If the parameter is a title of a sheet, we need to get the data from this sheet
        if parameter in self.workbook.keys():
            value_of_the_parameter = self.workbook['Global'].get_value_of_var_by_index_and_param(self.hostname, parameter)
            data = self.workbook[parameter].get_all_param_by_index(value_of_the_parameter)
            local_templates = self.workbook[parameter].get_local_templates()
            output = ''
            for template in local_templates:
                template_name = 'Template ' + template[0]
                if template_name in self.workbook[parameter].get_all_headers():
                    if self.workbook[parameter].get_value_of_var_by_index_and_param(value_of_the_parameter, template_name) == "Oui":
                        output += self.fill_local_template(self, data, template[1])
            return output
        # If the parameter/feature is only a variable (there is not a sheet for this feature)
        else:
            return self.workbook['Global'].get_value_of_var_by_index_and_param(self.hostname, parameter)

    @staticmethod
    def fill_local_template(self, data, local_template):
        is_braces = re.findall(self.pattern_contains_braces, local_template)
        if is_braces:
            for value in is_braces:
                local_template = local_template.replace(''.join(['{{', value, '}}']), data[value])
        return local_template

    def get_value_of_var_with_exclamation_and_colon(self, var_with_exclamation_and_colon, workbook):
        is_brackets = re.findall(self.pattern_contains_brackets, var_with_exclamation_and_colon)
        if is_brackets:
            for pattern_with_brackets in is_brackets:
                value = self.get_value_of_var_with_exclamation_and_colon(pattern_with_brackets, workbook)
                var_with_exclamation_and_colon = re.sub(self.pattern_contains_brackets,
                                                        value,
                                                        var_with_exclamation_and_colon)
        # We need to remove braces if this method is called for local templates
        if re.findall(self.pattern_contains_braces, var_with_exclamation_and_colon):
            var_with_exclamation_and_colon = self.remove_braces(var_with_exclamation_and_colon)
        splitted_var = re.split("[!,:]+", var_with_exclamation_and_colon)
        instance_of_object = workbook[splitted_var[0]]
        if isinstance(instance_of_object, ArrayParsing):
            value = workbook[splitted_var[0]].get_value_of_var_by_index_and_param(splitted_var[1], splitted_var[2])
            if value is None:
                self.unresolved += 1
                return "<unresolved>"
            else:
                return value
        elif isinstance(instance_of_object, ListParsing):
            value = workbook[splitted_var[0]].get_value_by_bag_and_key_and_index(splitted_var[1],
                                                                                 splitted_var[2],
                                                                                 int(splitted_var[3]))
            if value is None:
                self.unresolved += 1
                return "<unresolved>"
            else:
                return value
        elif isinstance(instance_of_object, TextParsing):
            value = workbook[splitted_var[0]].get_text_by_title(splitted_var[1])
            if value is None:
                self.unresolved += 1
                return "<unresolved>"
            else:
                return value
        else:
            self.unresolved += 1
            return "<unresolved>"

    def get_value_of_var_with_interrogation(self, var_with_interrogation, workbook):
        splitted_var = re.split("[?]+", var_with_interrogation)
        if splitted_var[0] in workbook['Global'].get_all_headers() and splitted_var[0] in self.workbook.keys():
            return workbook[splitted_var[0]].get_value_of_var_by_index_and_param(
                workbook['Global'].get_value_of_var_by_index_and_param(self.hostname, splitted_var[0]),
                splitted_var[1])
        else:
            self.unresolved += 1
            return "<unresolved>"

    @staticmethod
    def remove_braces(string):
        return string[2:-2]

    def get_unresolved_var(self):
        return int(self.unresolved)
