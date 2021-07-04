import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import blockService as BlockService


class TestResetBlock(unittest.TestCase):

    def test_reset_block_with_prev_number(self):
        block = {
            "prev_number": "0xc2567d"
        }
        BlockService.reset_block(block)
        self.assertDictEqual(block, {})

    def test_reset_block_with_next_number(self):
        block = {
            "next_number": "0xc2567d"
        }
        BlockService.reset_block(block)
        self.assertDictEqual(block, {})

    def test_reset_block_with_position(self):
        block = {
            "position": "head"
        }
        BlockService.reset_block(block)
        self.assertDictEqual(block, {})

    def test_reset_block_with_all(self):
        block = {
            "prev_number": "0xc2567d",
            "next_number": "0xc2567d",
            "position": "head"
        }
        BlockService.reset_block(block)
        self.assertDictEqual(block, {})

    def test_reset_block_without_all(self):
        block = {
            "number": "0xc2567d"
        }
        BlockService.reset_block(block)
        self.assertDictEqual(block, {
            "number": "0xc2567d"
        })


if __name__ == "__main__":
    unittest.main()
