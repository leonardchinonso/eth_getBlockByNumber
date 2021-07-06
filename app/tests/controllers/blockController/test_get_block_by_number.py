import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.getenv("BASE_PATH"))

from app.controllers import blockController as BlockController


class TestGetBlockByNumber(unittest.TestCase):

    def test_get_block_by_number_returns_none(self):
        self.assertIsNone(BlockController.get_block_by_number("0x123412341234"))

    def test_get_block_by_number_returns_valid_block(self):
        data = BlockController.get_block_by_number("0x1234")
        self.assertIsNotNone(data)
        self.assertEqual("0x1234", data.number)


if __name__ == '__main__':
    unittest.main()
