import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.models.block import Block


class TestSetNextBlock(unittest.TestCase):

    def setUp(self) -> None:
        self.next_block = Block("0x1234", {
            "number": "0x1235"
        })
        self.block = Block("0x1234", {
            "number": "0x1234"
        })

    def test_set_next_block_is_successful(self):
        self.block.set_next_block(self.next_block)
        self.assertEqual(self.block.next_block, self.next_block)

    def test_set_next_block_sets_none(self):
        self.block.set_next_block(self.next_block)
        self.assertEqual(self.block.next_block, self.next_block)
        self.block.set_next_block(None)
        self.assertIsNone(self.block.next_block)


if __name__ == '__main__':
    unittest.main()
