import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import cacheService as CacheService


class TestGetCache(unittest.TestCase):

    def setUp(self) -> None:
        self.CAPACITY = int(os.getenv("CAPACITY"))

    def test_get_cache_returns_cache(self):
        cache = CacheService.get_cache()

        self.assertEqual(cache.get_capacity(), self.CAPACITY)
        self.assertEqual(cache.get_size(), 0)
        self.assertEqual(cache.head.number, "head")
        self.assertEqual(cache.tail.number, "tail")
        self.assertEqual(cache.head.next_block, cache.tail)
        self.assertEqual(cache.tail.prev_block, cache.head)
        self.assertIsNone(cache.head.data)
        self.assertIsNone(cache.tail.data)
        self.assertDictEqual(cache.data, {})
        self.assertDictEqual(cache.get_blocks(), {})


if __name__ == '__main__':
    unittest.main()
