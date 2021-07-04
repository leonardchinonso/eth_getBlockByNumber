import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import blockService as BlockService


class TestSetAdjacentBlock(unittest.TestCase):

    def setUp(self) -> None:
        self.block = {
            "position": "head",
        }

    def test_set_block_field_is_successful(self):
        BlockService.set_block_field(self.block, "prev_number", "0xc1234")
        self.assertDictEqual(self.block, {
            "position": "head",
            "prev_number": "0xc1234"
        })


if __name__ == "__main__":
    unittest.main()
