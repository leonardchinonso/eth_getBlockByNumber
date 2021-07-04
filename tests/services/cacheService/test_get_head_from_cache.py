import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import cacheService as CacheService


class TestGetHeadFromCache(unittest.TestCase):

    def setUp(self) -> None:
        self.cache = {
            "0x1": {
                "number": "0x1",
                "position": "head",
            }
        }

    def test_get_head_from_cache_returns_valid_block(self):
        head = CacheService.get_head_from_cache(self.cache)
        self.assertEqual(head, {
            "number": "0x1",
            "position": "head",
        })

    def test_get_head_from_cache_returns_none(self):
        self.cache["0x1"]["position"] = "tail"
        self.assertIsNone(CacheService.get_head_from_cache(self.cache))


if __name__ == '__main__':
    unittest.main()
