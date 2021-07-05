import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.models.block import Block


class TestBlockInitialization(unittest.TestCase):

    def setUp(self) -> None:
        self.prev_block = Block("0x1234", {
            "number": "0x1233"
        })
        self.block = Block("0x1234", {
            "number": "0x1234"
        }, self.prev_block)

    def test_block_initialises_successfully(self):
        self.assertEqual(self.block.number, "0x1234")
        self.assertIsNone(self.block.next_block)
        self.assertEqual(self.block.prev_block, self.prev_block)
        self.assertDictEqual(self.block.data, {
            "number": "0x1234"
        })

    def test_block_not_initialising_successfully(self):
        with self.assertRaises(TypeError):
            self.block = Block("0x1234")


if __name__ == "__main__":
    unittest.main()
