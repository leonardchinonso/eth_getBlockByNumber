import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.models.block import Block


class TestGetNextBlock(unittest.TestCase):

    def setUp(self) -> None:
        self.next_block = Block("0x1234", {
            "number": "0x1235"
        })
        self.block = Block("0x1234", {
            "number": "0x1234"
        }, None, self.next_block)

    def test_get_next_block_returns_block(self):
        self.assertEqual(self.block.get_next_block(), self.next_block)

    def test_get_next_block_returns_none(self):
        self.block.next_block = None
        self.assertIsNone(self.block.get_next_block())


if __name__ == '__main__':
    unittest.main()
