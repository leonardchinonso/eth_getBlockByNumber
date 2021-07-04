import os
import sys
import json
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import cacheService as CacheService


class TestAddToHeadOfCache(unittest.TestCase):

    def setUp(self) -> None:
        self.path = os.path.join(os.getenv("BASE_PATH"), "app/models/cache.json")

        self.cache = {
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
        }

        self.block = {
            "number": "0x1"
        }

        self.latest_block = {
            "number": "0x22"
        }

    def get_cache(self):
        self.cache_file = open(self.path, "r")

        data = self.cache_file.read()

        self.cache_file.close()

        return json.loads(data)

    def test_add_to_head_of_empty_cache(self):
        self.cache = {}

        CacheService.add_to_head_of_cache(self.block, self.latest_block, self.cache)

        cache_file = self.get_cache()

        self.assertDictEqual(cache_file, {
            "0x1": {
                "position": "head",
                "number": "0x1"
            }
        })

    def test_add_to_head_of_cache_with_one_item(self):
        del self.cache["0x3"]
        del self.cache["0x2"]["next_number"]

        CacheService.add_to_head_of_cache(self.block, self.latest_block, self.cache)

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

    def test_add_to_head_of_cache_with_more_than_one_item(self):
        CacheService.add_to_head_of_cache(self.block, self.latest_block, self.cache)

        cache_file = self.get_cache()

        self.assertDictEqual(cache_file, {
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
            }
        })


if __name__ == "__main__":
    unittest.main()
