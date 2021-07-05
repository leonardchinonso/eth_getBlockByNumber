import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import cacheService as CacheService


class TestIsWithinLatestBlock(unittest.TestCase):

    def setUp(self) -> None:
        self.block_number = "0x1"  # 1
        self.latest_block_number = "0x16"  # 22

    def test_is_within_latest_block_returns_false(self):
        self.assertFalse(CacheService.is_within_latest_block(self.block_number, self.latest_block_number))

    def test_is_within_latest_block_returns_true(self):
        self.block_number = "0x3"  # 3
        self.assertTrue(CacheService.is_within_latest_block(self.block_number, self.latest_block_number))


if __name__ == "__main__":
    unittest.main()
