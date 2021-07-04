import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services import blockService as BlockService


class TestSetBlockPosition(unittest.TestCase):

    def setUp(self) -> None:
        self.block = {
            "prev_number": "0xc1234",
        }

    def test_set_block_position_is_successful(self):
        BlockService.set_block_position(self.block, "tail")
        self.assertDictEqual(self.block, {
            "position": "tail",
            "prev_number": "0xc1234"
        })


if __name__ == "__main__":
    unittest.main()
