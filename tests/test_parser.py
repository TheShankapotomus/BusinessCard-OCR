import json
import unittest
from os.path import dirname, realpath
from ocr import BusinessCardParser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = BusinessCardParser()

    def tearDown(self):
        del self.parser

    def test_asymmetrik(self):
        self._check_examples(f"{dirname(realpath(__file__))}/examples/asymmetrik.json")

    def test_custom(self):

        self._check_examples(f"{dirname(realpath(__file__))}/examples/custom.json")

    def _check_examples(self, file):

        with open(file, 'r') as f:
            examples = json.load(f)

        for e in examples:

            contact_info = str(self.parser.get_contact_info(e["document"]))
            self.assertEqual(e["output"], contact_info)
