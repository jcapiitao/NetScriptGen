# -*-coding:UTF-8 -*

from unittest import TestCase
from process.TextParsing import TextParsing
from utils.ExcelWorkbookManager import get_sheet_test


class TextParsingTests(TestCase):

    def setUp(self):
        self.sheet = TextParsing(get_sheet_test('textparsing_test.xlsx'))

    def test_get_text_by_title(self):
        expected = 'test'
        got = self.sheet.get_text_by_title('banner')
        self.assertEqual(expected, got)

    def test_get_text_by_title_failed(self):
        expected = KeyError
        got = self.sheet.get_text_by_title('invalid_title')
        self.assertRaises(expected, got)

    def test_get_all_titles(self):
        expected = ['banner', 'password', 'name']
        got = self.sheet.get_all_titles()
        self.assertListEqual(expected, got)

    def test_is_title_true(self):
        expected = True
        got = self.sheet.is_title('password')
        self.assertEqual(expected, got)

    def test_is_title_false(self):
        expected = False
        got = self.sheet.is_title('invalid_title')
        self.assertEqual(expected, got)
