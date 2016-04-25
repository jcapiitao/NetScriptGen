# -*-coding:UTF-8 -*

import re
import os
import sys
import traceback
from process.ArrayParsing import ArrayParsing
from process.TextParsing import TextParsing
from process.ListParsing import ListParsing


class Equipment(object):

    def __init__(self, hostname, template, workbook):
        self.hostname = hostname
        self.template = template
        self.workbook = workbook
        self.unresolved = 0
        self.resolved = 0
        self.tb = list()
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
        with open(os.path.join(path_of_the_folder, file_name) + extension, "w") as file:
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
            data_of_the_parameter = self.workbook[parameter].get_all_param_by_index(value_of_the_parameter)
            template_regex = re.compile('template')
            output = ''
            for _header, _template_name in data_of_the_parameter.items():
                if template_regex.match(_header.lower()):
                    template_content = self.workbook[parameter].template_content_by_name(_template_name.lower())
                    output += self.fill_local_template(self, data_of_the_parameter, template_content)
            if output == '':
                self.unresolved += 1
                self.tb += traceback.format_exception_only(FileExistsError,
                                                           "No subtemplates in sheet '{}'".format(parameter))
                return "<unresolved>"
            else:
                return output
        # If the parameter/feature is only a variable (there is not a sheet for this feature)
        else:
            try:
                value = self.workbook['Global'].get_value_of_var_by_index_and_param(self.hostname, parameter)
                self.resolved += 1
                return value
            except KeyError as err:
                self.unresolved += 1
                self.tb += traceback.format_exception_only(KeyError, err)
                return "<unresolved>"

    @staticmethod
    def fill_local_template(self, data, local_template):
        is_braces = re.findall(self.pattern_contains_braces, local_template)
        if is_braces:
            for value in is_braces:
                if value in data:
                    local_template = local_template.replace(''.join(['{{', value, '}}']), data[value])
                    self.resolved += 1
                else:
                    local_template = local_template.replace(''.join(['{{', value, '}}']),
                                                            self.get_value_of_var(value, self.workbook))
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
            try:
                value = workbook[splitted_var[0]].get_value_of_var_by_index_and_param(splitted_var[1], splitted_var[2])
                self.resolved += 1
                return value
            except KeyError as err:
                self.unresolved += 1
                self.tb += traceback.format_exception_only(KeyError, err)
                return "<unresolved>"
        elif isinstance(instance_of_object, ListParsing):
            try:
                value = workbook[splitted_var[0]].get_value_by_bag_and_key_and_index(splitted_var[1],
                                                                                 splitted_var[2],
                                                                                 int(splitted_var[3]))
                self.resolved += 1
                return value
            except KeyError as err:
                self.unresolved += 1
                self.tb += traceback.format_exception_only(KeyError, err)
                return "<unresolved>"
        elif isinstance(instance_of_object, TextParsing):
            try:
                value = workbook[splitted_var[0]].get_text_by_title(splitted_var[1])
                self.resolved += 1
                return value
            except KeyError as err:
                self.unresolved += 1
                self.tb += traceback.format_exception_only(KeyError, err)
                return "<unresolved>"
        else:
            err = "No match found for this variable '{0}'".format(var_with_exclamation_and_colon)
            self.tb += traceback.format_exception_only(KeyError, err)
            self.unresolved += 1
            return "<unresolved>"

    def get_value_of_var_with_interrogation(self, var_with_interrogation, workbook):
        splitted_var = re.split("[?]+", var_with_interrogation)
        try:
            value = workbook[splitted_var[0]].get_value_of_var_by_index_and_param(
            workbook['Global'].get_value_of_var_by_index_and_param(self.hostname, splitted_var[0]), splitted_var[1])
            self.resolved += 1
            return value
        except KeyError as err:
            self.unresolved += 1
            self.tb += traceback.format_exception_only(KeyError, err)
            return "<unresolved>"


    @staticmethod
    def remove_braces(string):
        return string[2:-2]

    def get_unresolved_var(self):
        return int(self.unresolved)

    def get_resolved_var(self):
        return int(self.resolved)

    def get_filling_ratio(self):
        return '{0}/{1}'.format(int(self.resolved),((int(self.resolved) + int(self.unresolved))))

    def get_filling_ratio_in_percentage(self):
        return '{:.0%}'.format(int(self.resolved)/(int(self.resolved) + int(self.unresolved)))

    def get_nbr_of_var_to_fill_in(self):
        return int(self.resolved + self.unresolved)
