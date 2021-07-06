import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.getenv("BASE_PATH"))

from app.models.block import Block


class TestGetPrevBlock(unittest.TestCase):

    def setUp(self) -> None:
        self.prev_block = Block("0x1234", {
            "number": "0x1233"
        })
        self.block = Block("0x1234", {
            "number": "0x1234"
        }, self.prev_block)

    def test_get_prev_block_returns_block(self):
        self.assertEqual(self.block.get_prev_block(), self.prev_block)

    def test_get_prev_block_returns_none(self):
        self.block.prev_block = None
        self.assertIsNone(self.block.get_prev_block())


if __name__ == '__main__':
    unittest.main()
