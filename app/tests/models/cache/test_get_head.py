import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.models.cache import Cache
from app.models.block import Block


class TestGetHead(unittest.TestCase):

    def setUp(self) -> None:
        self.cache = Cache(5)
        self.block = Block("0x1234", None)

    def add_block(self):
        temp = self.cache.tail
        self.cache.head.next_block = self.block
        self.block.prev_block = self.cache.head
        self.block.next_block = temp
        temp.prev_block = self.block
        self.cache.set_size(1)

    def test_get_head_when_cache_is_empty(self):
        self.assertIsNone(self.cache.get_head())

    def test_get_head_when_cache_contains_block(self):
        self.add_block()
        self.assertEqual(self.block.next_block, self.cache.tail)
        self.assertEqual(self.block.prev_block, self.cache.head)
        self.assertEqual(self.cache.head.next_block, self.block)
        self.assertEqual(self.cache.tail.prev_block, self.block)
        self.assertEqual(self.cache.get_size(), 1)
        self.assertEqual(self.cache.get_head(), self.block)


if __name__ == '__main__':
    unittest.main()
