import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import cacheService as CacheService


class TestRemoveBlockByNumber(unittest.TestCase):

    def test_remove_block_by_number_is_successful(self):
        cache = {
            "0x1234": {}
        }

        CacheService.remove_block_by_number("0x1234", cache)

        self.assertEqual(cache, {})


if __name__ == '__main__':
    unittest.main()
