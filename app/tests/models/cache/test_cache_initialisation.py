import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.getenv("BASE_PATH"))

from app.models.cache import Cache
from app.services.errorService import ErrorHandler


class TestCacheInitialisation(unittest.TestCase):

    def setUp(self) -> None:
        self.cache = Cache(5)

    def test_cache_initialises_successfully(self):
        self.assertEqual(self.cache.head.number, "head")
        self.assertEqual(self.cache.tail.number, "tail")
        self.assertIsNone(self.cache.head.data)
        self.assertIsNone(self.cache.tail.data)
        self.assertDictEqual(self.cache.data, {})
        self.assertDictEqual(self.cache.get_blocks(), {})
        self.assertEqual(self.cache.head.next_block, self.cache.tail)
        self.assertEqual(self.cache.tail.prev_block, self.cache.head)
        self.assertEqual(self.cache.get_capacity(), 5)
        self.assertEqual(self.cache.get_size(), 0)

    def test_cache_initialisation_raises_error(self):
        with self.assertRaises(ErrorHandler) as ContextManager:
            self.cache = Cache(1)

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "Capacity cannot be less than or equal to 1!")


if __name__ == '__main__':
    unittest.main()
