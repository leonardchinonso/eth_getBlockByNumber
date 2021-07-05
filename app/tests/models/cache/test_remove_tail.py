import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.models.cache import Cache
from app.models.block import Block
from app.services.errorService import ErrorHandler


class TestRemoveTail(unittest.TestCase):

    def setUp(self) -> None:
        self.cache = Cache(5)
        self.block1 = Block("0x1", {
            "number": "0x1"
        })
        self.block2 = Block("0x2", {
            "number": "0x2"
        })

    def add_block(self, prev, block, nextt):
        prev.next_block = block
        block.prev_block = prev
        block.next_block = nextt
        nextt.prev_block = block

        self.cache.data[block.number] = block.data
        self.cache.add_block_data_to_blocks(block)
        self.cache.set_size(self.cache.get_size() + 1)

    def test_remove_tail_when_cache_has_one_block(self):
        self.add_block(self.cache.head, self.block1, self.cache.tail)

        with self.assertRaises(ErrorHandler) as ContextManager:
            self.cache.remove_tail()

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "You cannot remove a tail from cache with size equal to or less than 1!")

    def test_remove_tail_when_cache_has_multiple_blocks(self):
        self.add_block(self.cache.head, self.block1, self.cache.tail)
        self.add_block(self.block1, self.block2, self.cache.tail)

        self.assertEqual(self.cache.head.next_block, self.block1)
        self.assertEqual(self.cache.tail.prev_block, self.block2)

        self.cache.remove_tail()
        self.assertEqual(self.cache.head.next_block, self.block1)
        self.assertEqual(self.cache.tail.prev_block, self.block1)


if __name__ == '__main__':
    unittest.main()
