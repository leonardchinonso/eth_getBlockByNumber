import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services.errorService import ErrorHandler
from app.services import cacheService as CacheService


class TestRemoveTailFromCache(unittest.TestCase):

    def setUp(self) -> None:
        self.cache = {
            "0x1": {
                "number": "0x1",
                "position": "head",
                "next_number": "0x2"
            },
            "0x2": {
                "number": "0x2",
                "position": "mid",
                "prev_number": "0x1",
                "next_number": "0x3"
            },
            "0x3": {
                "number": "0x3",
                "position": "tail",
                "prev_number": "0x2"
            },
        }

    def test_cache_has_tail_and_prev_block(self):
        CacheService.remove_tail_from_cache(self.cache)
        self.assertDictEqual(self.cache, {
            "0x1": {
                "number": "0x1",
                "position": "head",
                "next_number": "0x2"
            },
            "0x2": {
                "number": "0x2",
                "position": "tail",
                "prev_number": "0x1"
            }
        })

    def test_cache_has_tail_and_no_prev_block(self):
        del self.cache["0x3"]["prev_number"]

        with self.assertRaises(ErrorHandler) as ContextManager:
            CacheService.remove_tail_from_cache(self.cache)

            exception = ContextManager.exception
            self.assertEqual(exception.status_code, 500)
            self.assertEqual(exception.message, "Tail has no previous block!")

    def test_cache_has_no_tail_and_cache_length_is_greater_than_one(self):
        self.cache["0x3"]["position"] = "mid"

        with self.assertRaises(ErrorHandler) as ContextManager:
            CacheService.remove_tail_from_cache(self.cache)

            exception = ContextManager.exception
            self.assertEqual(exception.status_code, 500)
            self.assertEqual(exception.message, "Cache has no tail!")


if __name__ == '__main__':
    unittest.main()
