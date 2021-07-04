import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.controllers import blockController as BlockController


class TestGetBlockByNumberFromCache(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = {
            "0xc1234": {
                "number": "0xc1234"
            }
        }

    def test_get_block_by_number_from_cache_returns_none(self):
        self.assertIsNone(BlockController.get_block_by_number_from_cache("0xc1111", self.cache))

    def test_get_block_by_number_from_cache_returns_valid_block(self):
        self.assertDictEqual(BlockController.get_block_by_number_from_cache("0xc1234", self.cache), {
                "number": "0xc1234"
            })


if __name__ == '__main__':
    unittest.main()
