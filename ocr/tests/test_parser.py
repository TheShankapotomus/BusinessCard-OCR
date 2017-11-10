import json
import os
import unittest
from ocr import BusinessCardParser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = BusinessCardParser()

    def test_asymmetrik(self):

        with open(f"{os.getcwd()}/asymmetrik.json", 'r') as f:

            examples = json.load(f)

        for e in examples:

            contact_info= str(self.parser.get_contact_info(e["document"]))
            self.assertEqual(e["output"], contact_info)

    def test_custom(self):
        pass