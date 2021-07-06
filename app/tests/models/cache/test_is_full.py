import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.getenv("BASE_PATH"))

from app.models.cache import Cache


class TestIsFull(unittest.TestCase):

    def setUp(self) -> None:
        self.cache = Cache(5)

    def test_is_full_returns_false(self):
        self.assertFalse(self.cache.is_full())

    # WARNING: The Cache.set_size() method is only exposed so this test check can be made.
    # The size property of a cache is a private property and should not be changed from outside its class
    def test_is_full_returns_true(self):
        self.cache.set_size(5)
        self.assertTrue(self.cache.is_full())


if __name__ == '__main__':
    unittest.main()
