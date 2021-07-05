import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.models.cache import Cache
from app.models.block import Block
from app.services.errorService import ErrorHandler


class TestRemoveBlock(unittest.TestCase):

    def setUp(self) -> None:
        self.cache = Cache(5)
        self.block = Block("0x1234", {
            "number": "0x1234"
        })

    def add_block(self):
        temp = self.cache.tail
        self.cache.head.next_block = self.block
        self.block.prev_block = self.cache.head
        self.block.next_block = temp
        temp.prev_block = self.block

        self.cache.data[self.block.number] = self.block.data
        self.cache.add_block_data_to_blocks(self.block)
        self.cache.set_size(1)

    def test_remove_block_from_empty_cache(self):
        with self.assertRaises(ErrorHandler) as ContextManager:
            self.cache.remove_block(self.block)

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "Cannot remove block from an empty cache!")

    def test_remove_block_from_non_empty_cache(self):
        self.add_block()
        self.assertEqual(self.block.next_block, self.cache.tail)
        self.assertEqual(self.block.prev_block, self.cache.head)
        self.assertEqual(self.cache.head.next_block, self.block)
        self.assertEqual(self.cache.tail.prev_block, self.block)
        self.assertDictEqual(self.cache.data, {
            "0x1234": {
                "number": "0x1234"
            }
        })
        self.assertDictEqual(self.cache.get_blocks(), {
            "0x1234": self.block
        })

        self.cache.remove_block(self.block)
        self.assertEqual(self.cache.head.next_block, self.cache.tail)
        self.assertEqual(self.cache.tail.prev_block, self.cache.head)
        self.assertDictEqual(self.cache.data, {})
        self.assertDictEqual(self.cache.get_blocks(), {})
        self.assertEqual(self.cache.get_size(), 0)


if __name__ == '__main__':
    unittest.main()
