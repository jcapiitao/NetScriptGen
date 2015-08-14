# -*-coding:UTF-8 -*

import re
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
        self.pattern_contains_exclamation_and_colon = '[!,:]'

    def get_script(self):
        script = self.fill_out_the_template()
        if self.unresolved != 0:
            line = "! ----- Warning : There is %s unresolved variable -----\n" % self.unresolved
            script = line + script
        return script

    def fill_out_the_template(self):
        pattern_to_fill = re.findall(self.pattern_contains_braces, self.template)
        template = self.template
        if pattern_to_fill:
            for pattern in pattern_to_fill:
                template = template.replace(''.join(['{{', pattern, '}}']),
                                            self.get_value_of_var(pattern, self.workbook))
        return template

    def save_script_as(self, path_of_the_folder, file_name):
        extension = '.txt'
        with open(path_of_the_folder + '/' + file_name + extension, "w") as file:
            file.write(self.get_script())
        file.close()

    def get_value_of_var(self, pattern, workbook):
        if re.findall(self.pattern_contains_exclamation_and_colon, pattern):
            return self.get_var_with_exclamation_and_colon(pattern, workbook)
        else:
            return self.get_var_from_global_sheet(pattern)

    def get_var_from_global_sheet(self, parameter):
        # If the parameter is a title of a sheet, we need to get data from this sheet
        # parameter = self.remove_braces(parameter)
        if parameter in self.workbook.keys():
            index = self.workbook['Global'].get_param_by_index(self.hostname, parameter)
            data = self.workbook[parameter].get_all_param_by_index(index)
            local_templates = self.workbook[parameter].get_local_templates()
            output = ''
            for template in local_templates:
                template_name = 'Template ' + template[0]
                if template_name in self.workbook[parameter].get_all_headers():
                    if self.workbook[parameter].get_param_by_index(index, template_name) == "Oui":
                        output += self.fill_local_template(self, data, template[1])
            return output
        else:
            return self.workbook['Global'].get_param_by_index(self.hostname, parameter)

    @staticmethod
    def fill_local_template(self, data, local_template):
        is_brackets = re.findall(self.pattern_contains_braces, local_template)
        if is_brackets:
            for value in is_brackets:
                local_template = local_template.replace(''.join(['{{', value, '}}']), data[value])
        return local_template

    def get_var_with_exclamation_and_colon(self, pattern, workbook):
        is_brackets = re.findall(self.pattern_contains_brackets, pattern)
        if is_brackets:
            for pattern_with_brackets in is_brackets:
                value = self.get_var_with_exclamation_and_colon(pattern_with_brackets, workbook)
                pattern = re.sub(self.pattern_contains_brackets, value, pattern)
        if re.findall(self.pattern_contains_braces, pattern):
            pattern = self.remove_braces(pattern)
        split_pattern = re.split("[!,:]+", pattern)
        instance_of_object = workbook[split_pattern[0]]
        if isinstance(instance_of_object, ArrayParsing):
            result = workbook[split_pattern[0]].get_param_by_index(split_pattern[1], split_pattern[2])
            if result is None:
                self.unresolved += 1
                return "<unresolved>"
            else:
                return result
        elif isinstance(instance_of_object, ListParsing):
            result = workbook[split_pattern[0]].get_value_by_bag_and_key_and_index(split_pattern[1], split_pattern[2],
                                                                                   int(split_pattern[3]))
            if result is None:
                self.unresolved += 1
                return "<unresolved>"
            else:
                return result
        elif isinstance(instance_of_object, TextParsing):
            result = workbook[split_pattern[0]].get_text_by_title(split_pattern[1])
            if result is None:
                self.unresolved += 1
                return "<unresolved>"
            else:
                return result
        else:
            self.unresolved += 1
            return "<unresolved>"

    @staticmethod
    def remove_braces(string):
        return string[2:-2]

    def get_unresolved_var(self):
        return int(self.unresolved)
