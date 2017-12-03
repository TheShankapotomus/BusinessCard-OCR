import logging
import unittest
import yaml
from os.path import dirname, realpath
from ocr import BusinessCardParser


logger = logging.getLogger(__name__)

class TestParser(unittest.TestCase):
    """A tester for the parser module with BusinessCardParser"""

    def setUp(self):
        """Setup the TestCase prior to execution"""
        self.parser = BusinessCardParser()
        logger.debug(f"Setting up {self.__class__}")

    def tearDown(self):
        """Formally delete internal object attributes"""
        logger.debug(f"Tearing down {self.__class__}")
        del self.parser

    def test_asymmetrik(self):
        """Run the ./samples/asymmetrik.yaml test set"""
        logger.info(f"Running Asymmetrik samples test!")
        self._check_examples(f"{dirname(realpath(__file__))}/samples/asymmetrik.yaml")

    def test_custom(self):
        """Run the ./samples/custom.yaml test set"""
        logger.info(f"Running custom samples test!")
        self._check_examples(f"{dirname(realpath(__file__))}/samples/custom.yaml")

    def _check_examples(self, file):
        """Load a set of tests and run them through the BusinessCardParser

        Note
        ----
        Load a YAML test file and test the processed documents against
        there expected output.

        Parameters
        ----------
        file : str
            The test file path to load

        """
        with open(file, 'r') as f:
            examples = yaml.safe_load(f).values()

        for i,e in enumerate(examples):

            i += 1
            contact_info = str(self.parser.get_contact_info(e["document"]))
            self.assertEqual(e["output"], contact_info)

            logger.info(f"\n---Test {str(i)}---\n\nDocument parsed: \n\n{e['document']}\n\n"
                        f"Expected output: \n\n{e['output']}\n\n"
                        f"Info parsed: \n\n{contact_info}\n\n"
                        f"Test {str(i)} State: {'PASS' if e['output'] == contact_info else 'FAIL'}\n\n"
                        "-----------------------------------------------------\n")