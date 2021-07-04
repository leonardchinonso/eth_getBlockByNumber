import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services.errorService import ErrorHandler
from app.services import cacheService as CacheService


class TestCacheIsFull(unittest.TestCase):

    def setUp(self) -> None:
        CAPACITY = int(os.getenv("CAPACITY"))
        if CAPACITY <= 1:
            raise ErrorHandler("Capacity cannot be less than 1", status_code=500)
        self._set = set(range(CAPACITY))
        self.cache = dict.fromkeys(self._set)

    def test_cache_is_full_returns_true(self):
        self.assertTrue(CacheService.cache_is_full(self.cache))

    def test_cache_is_full_returns_false(self):
        del self.cache[0]
        self.assertFalse(CacheService.cache_is_full(self.cache))


if __name__ == '__main__':
    unittest.main()
