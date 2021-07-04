import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import utilService as UtilService
from app.services.errorService import ErrorHandler


class TestConvertHexToInteger(unittest.TestCase):

    def test_successful_conversion(self):
        self.assertEqual(UtilService.convert_hex_to_int("0xc2687"), int("0xc2687", 16))

    def test_failed_conversion(self):
        with self.assertRaises(ErrorHandler) as ContextManager:
            UtilService.convert_hex_to_int("0xc268g")

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "Invalid hexadecimal number!")


if __name__ == "__main__":
    unittest.main()
