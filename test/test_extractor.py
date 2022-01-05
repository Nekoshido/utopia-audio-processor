from setuptools import find_packages

from src.extractor import Extractor
from unittest import TestCase


class ExctractorTest(TestCase):
    extractor = Extractor()

    def test_normalize_unicode_to_ascii(self):
        input_string = "Mickæël"
        expected = 'mickel'

        real = self.file_processer._normalize_unicode_to_ascii(input_string)
        assert real == expected


