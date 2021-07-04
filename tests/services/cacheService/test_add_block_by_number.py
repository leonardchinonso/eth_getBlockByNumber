import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import cacheService as CacheService


class TestAddBlockByNumber(unittest.TestCase):

    def test_add_block_by_number_is_successful(self):
        cache = {}
        block = {
            "number": "0x1234"
        }

        CacheService.add_block_by_number("0x1234", cache, block)

        self.assertEqual(cache, {
            "0x1234": {
                "number": "0x1234"
            }
        })


if __name__ == '__main__':
    unittest.main()
