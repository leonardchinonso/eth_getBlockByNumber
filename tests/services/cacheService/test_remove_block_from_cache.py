import os
import sys
import json
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import cacheService as CacheService


class TestRemoveBlockFromCache(unittest.TestCase):

    def setUp(self) -> None:
        self.path = os.path.join(os.getenv("BASE_PATH"), "app/models/cache.json")
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

    def tearDown(self) -> None:
        self.cache_file = open(self.path, "w")
        self.cache_file.close()

    def get_cache(self):
        self.cache_file = open(self.path, "r")
        data = self.cache_file.read()
        self.cache_file.close()
        return json.loads(data)

    def test_remove_block_from_cache_when_block_is_head(self):
        block = {
            "number": "0x1",
            "position": "head",
            "next_number": "0x2"
        }

        CacheService.remove_block_from_cache(block, self.cache)

        cache_file = self.get_cache()

        self.assertDictEqual(cache_file, {
            "0x2": {
                "number": "0x2",
                "position": "head",
                "next_number": "0x3"
            },
            "0x3": {
                "number": "0x3",
                "position": "tail",
                "prev_number": "0x2"
            }
        })

    def test_remove_block_from_cache_when_block_is_mid(self):
        block = {
            "number": "0x2",
            "position": "mid",
            "prev_number": "0x1",
            "next_number": "0x3"
        }

        CacheService.remove_block_from_cache(block, self.cache)

        cache_file = self.get_cache()

        self.assertDictEqual(cache_file, {
            "0x1": {
                "number": "0x1",
                "position": "head",
                "next_number": "0x3"
            },
            "0x3": {
                "number": "0x3",
                "position": "tail",
                "prev_number": "0x1"
            },
        })

    def test_remove_block_from_cache_when_block_is_tail(self):
        block = {
            "number": "0x3",
            "position": "tail",
            "prev_number": "0x2"
        }

        CacheService.remove_block_from_cache(block, self.cache)

        cache_file = self.get_cache()

        self.assertDictEqual(cache_file, {
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


if __name__ == '__main__':
    unittest.main()
