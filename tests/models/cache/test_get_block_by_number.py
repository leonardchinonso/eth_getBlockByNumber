import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.models.cache import Cache
from app.models.block import Block


class TestGetBlockByNumber(unittest.TestCase):

    def setUp(self) -> None:
        self.cache = Cache(5)
        self.block = Block("0x1234", {
            "number": "0x1234"
        })

    def add_block(self, prev, block, nextt):
        prev.next_block = block
        block.prev_block = prev
        block.next_block = nextt
        nextt.prev_block = block

        self.cache.data[block.number] = block.data
        self.cache.add_block_data_to_blocks(block)
        self.cache.set_size(self.cache.get_size() + 1)

    def test_get_block_by_number_returns_data(self):
        self.add_block(self.cache.head, self.block, self.cache.tail)
        self.assertEqual(self.cache.get_block_by_number("0x1234"), self.block)

    def test_get_block_by_number_returns_none(self):
        self.assertIsNone(self.cache.get_block_by_number("0x1234"))


if __name__ == '__main__':
    unittest.main()
