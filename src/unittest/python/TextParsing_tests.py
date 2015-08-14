# -*-coding:UTF-8 -*

from unittest import TestCase
from process.TextParsing import TextParsing
from utils.ExcelWorkbookManager import get_sheet_test


class TextParsingTests(TestCase):

    def setUp(self):
        self.sheet = TextParsing(get_sheet_test('textparsing_test.xlsx'))

    def test_get_text_by_title(self):
        self.assertEqual(self.sheet.get_text_by_title('banner'), 'test')

    def test_get_text_by_title_failed(self):
        self.assertRaises(KeyError, self.sheet.get_text_by_title('invalid_title'))

    def test_get_all_titles(self):
        ref_list = ['banner', 'password', 'name']
        self.assertListEqual(ref_list, self.sheet.get_all_titles())

    def test_is_title_true(self):
        self.assertEqual(self.sheet.is_title('password'), True)

    def test_is_title_false(self):
        self.assertEqual(self.sheet.is_title('invalid_title'), False)
