import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.getenv("BASE_PATH"))

from app.models.block import Block


class TestSetPrevBlock(unittest.TestCase):

    def setUp(self) -> None:
        self.prev_block = Block("0x1234", {
            "number": "0x1233"
        })
        self.block = Block("0x1234", {
            "number": "0x1234"
        })

    def test_set_prev_block_is_successful(self):
        self.block.set_prev_block(self.prev_block)
        self.assertEqual(self.block.prev_block, self.prev_block)

    def test_set_prev_block_sets_none(self):
        self.block.set_prev_block(self.prev_block)
        self.assertEqual(self.block.prev_block, self.prev_block)
        self.block.set_prev_block(None)
        self.assertIsNone(self.block.prev_block)


if __name__ == '__main__':
    unittest.main()
