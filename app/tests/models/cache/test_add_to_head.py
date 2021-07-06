import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.getenv("BASE_PATH"))

from app.models.cache import Cache
from app.models.block import Block


class TestAddToHead(unittest.TestCase):

    def setUp(self) -> None:
        self.cache = Cache(2)
        self.block1 = Block("0x1", {
            "number": "0x1"
        })
        self.block2 = Block("0x2", {
            "number": "0x2"
        })
        self.block3 = Block("0x3", {
            "number": "0x3"
        })

    def test_add_to_head_when_cache_is_empty(self):
        self.cache.add_to_head(self.block1)

        self.assertEqual(self.block1.next_block, self.cache.tail)
        self.assertEqual(self.block1.prev_block, self.cache.head)
        self.assertEqual(self.cache.head.next_block, self.block1)
        self.assertEqual(self.cache.tail.prev_block, self.block1)
        self.assertDictEqual(self.cache.data, {
            "0x1": {
                "number": "0x1"
            }
        })
        self.assertDictEqual(self.cache.get_blocks(), {
            "0x1": self.block1
        })
        self.assertEqual(self.cache.get_size(), 1)

    def test_add_to_head_when_cache_has_items(self):
        self.cache.add_to_head(self.block1)
        self.cache.add_to_head(self.block2)

        self.assertEqual(self.cache.head.next_block, self.block2)
        self.assertEqual(self.block2.prev_block, self.cache.head)
        self.assertEqual(self.block2.next_block, self.block1)
        self.assertEqual(self.block1.prev_block, self.block2)
        self.assertEqual(self.block1.next_block, self.cache.tail)
        self.assertEqual(self.cache.tail.prev_block, self.block1)

        self.assertEqual(self.cache.get_size(), 2)

    def test_add_to_head_when_cache_is_full(self):
        self.cache.add_to_head(self.block1)
        self.cache.add_to_head(self.block2)
        self.cache.add_to_head(self.block3)

        self.assertEqual(self.cache.head.next_block, self.block3)
        self.assertEqual(self.block3.prev_block, self.cache.head)
        self.assertEqual(self.block3.next_block, self.block2)
        self.assertEqual(self.block2.prev_block, self.block3)
        self.assertEqual(self.block2.next_block, self.cache.tail)
        self.assertEqual(self.cache.tail.prev_block, self.block2)


if __name__ == '__main__':
    unittest.main()
