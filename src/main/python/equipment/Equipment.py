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
        self.pattern_to_fill_regexp = '{{.*}}'

    def get_script(self):
        script = self.fill_out_the_template(self.template, self.workbook)
        if self.unfilled_variable_counter != 0:
            line = "! /!\----- Warning : There is %s unfilled variable -----/!\\\n" % self.unfilled_variable_counter
            script = line + script
        return script

    def fill_out_the_template(self, template, workbook):
        pattern_to_fill = re.findall(self.pattern_to_fill_regexp, template)
        if pattern_to_fill:
            for pattern in pattern_to_fill:
                template = template.replace(pattern, self.get_value_of_pattern(self.remove_brackets(pattern), workbook))
        return template

    def save_script_as(self, path_of_the_folder, file_name):
        extension = '.txt'
        with open(path_of_the_folder + '/' + file_name + extension, "w") as file:
            file.write(self.get_script())
        file.close()

    def get_value_of_pattern(self, pattern, workbook):
        global unfilled_variable_counter
        splitPattern = re.split("[!,:]+", pattern)
        instanceOfSplitPattern = workbook[splitPattern[0]]
        if isinstance(instanceOfSplitPattern, ArrayParsing):
            result = workbook[splitPattern[0]].get_param_by_index(splitPattern[1], splitPattern[2])
            if result is KeyError:
                self.unfilled_variable_counter = self.unfilled_variable_counter + 1
                return "<unavailable to fill out>"
            else:
                return result
        elif isinstance(instanceOfSplitPattern, ListParsing):
            result = workbook[splitPattern[0]].get_value_by_bag_and_key_and_index(splitPattern[1], splitPattern[2],
                                                                                  int(splitPattern[3]))
            if result is KeyError:
                self.unfilled_variable_counter = self.unfilled_variable_counter + 1
                return "<unavailable to fill out>"
            else:
                return result
        elif isinstance(instanceOfSplitPattern, TextParsing):
            result = workbook[splitPattern[0]].get_text_by_title(splitPattern[1])
            if result is KeyError:
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

