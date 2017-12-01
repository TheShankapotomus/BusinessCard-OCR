import logging
import unittest
from argparse import ArgumentParser
from . import BusinessCardParser
from tests import TestParser


parser = ArgumentParser(description="Simple Business Card OCR")
parser.add_argument("-d", help="pass the document string to be parsed", type=str, dest="document")
parser.add_argument("--test", action="store_true", default=False, help="run test cases")
args = parser.parse_args()

if args.document:
    logging.basicConfig(level=logging.INFO)
    parser = BusinessCardParser()
    contact = parser.get_contact_info(args.document)

    logging.info(f"\n\nDocument passed: \n\n{args.document} \n\n"
                 f"Contact info parsed: \n\n{str(contact)}")

elif args.test:
    logging.basicConfig(level=logging.DEBUG)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestParser)
    runner = unittest.TextTestRunner()
    runner.run(suite)

else:
    parser.print_help()