import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import utilService as UtilService


class TestIsHash(unittest.TestCase):

    def test_is_hash_returns_true(self):
        self.assertTrue(UtilService.is_hash("0xbd4098c2fe1872584306928bf55c49518f44154634132e04453249180408ca3b"))

    def test_is_hash_returns_false(self):
        self.assertFalse(UtilService.is_hash("0xbd4098"))


if __name__ == "__main__":
    unittest.main()
