#!/usr/bin/python3
# -*-coding:UTF-8 -*

from process.ArrayParsing import ArrayParsing
from process.TextParsing import TextParsing
from process.ListParsing import ListParsing
import xlrd


class CiscoAccessSwitch(self):
    def __init__(self):
        self.hostname
        self.chassis
        self.is_stp = False
        self.is_vtp = False

