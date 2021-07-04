import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import blockService as BlockService
from app.services.errorService import ErrorHandler


class TestGetAdjacentBlock(unittest.TestCase):

    def setUp(self) -> None:
        self.head = {
            "position": "head",
            "next_number": "0xc2"
        }
        self.mid = {
            "prev_number": "0xc1",
            "position": "mid",
            "next_number": "0xc3"
        }
        self.tail = {
            "prev_number": "0xc2",
            "position": "mid",
        }
        self.cache = {
            "0xc1": self.head,
            "0xc2": self.mid,
            "0xc3": self.tail
        }

    def test_get_adjacent_block_returns_prev_block(self):
        prev_block = BlockService.get_adjacent_block(self.mid, "prev_number", self.cache)
        self.assertDictEqual(prev_block, self.head)

    def test_get_adjacent_block_returns_next_block(self):
        next_block = BlockService.get_adjacent_block(self.mid, "next_number", self.cache)
        self.assertDictEqual(next_block, self.tail)

    def test_get_adjacent_block_returns_none(self):
        next_block = BlockService.get_adjacent_block(self.tail, "next_number", self.cache)
        self.assertIsNone(next_block, None)

    def test_get_adjacent_block_raises_error(self):
        self.tail["prev_number"] = "0"
        with self.assertRaises(ErrorHandler) as ContextManager:
            BlockService.get_adjacent_block(self.tail, "prev_number", self.cache)

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "Cannot get adjacent cache!")
        self.assertEqual(exception.payload, self.tail)


if __name__ == "__main__":
    unittest.main()
