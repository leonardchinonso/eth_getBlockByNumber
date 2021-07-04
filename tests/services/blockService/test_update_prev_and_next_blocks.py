import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.services.errorService import ErrorHandler
from app.services import blockService as BlockService


class TestUpdatePrevAndNextBlocks(unittest.TestCase):

    def setUp(self) -> None:
        self.prev_block = {
            "prev_number": "0xc1",
            "next_number": "0xc3"
        }

        self.next_block = {
            "prev_number": "0xc4",
            "next_number": "0xc6"
        }

    def tearDown(self) -> None:
        self.prev_block = {
            "prev_number": "0xc1",
            "next_number": "0xc3"
        }

        self.next_block = {
            "prev_number": "0xc4",
            "next_number": "0xc6"
        }

    def test_position_is_head_and_next_block_is_not_none(self):
        BlockService.update_prev_and_next_blocks("head", None, self.next_block)

        self.assertDictEqual(self.next_block, {
            "position": "head",
            "next_number": "0xc6"
        })

    def test_position_is_tail_and_prev_block_is_none(self):
        with self.assertRaises(ErrorHandler) as ContextManager:
            BlockService.update_prev_and_next_blocks("tail", None, None)

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "Tail block has no previous!")

    def test_position_is_tail_and_prev_block_position_is_head(self):
        self.prev_block["position"] = "head"
        del self.prev_block["prev_number"]

        BlockService.update_prev_and_next_blocks("tail", self.prev_block, None)

        self.assertDictEqual(self.prev_block, {
            "position": "head"
        })

    def test_position_is_tail_and_prev_block_position_is_not_head(self):
        self.prev_block["position"] = "mid"
        BlockService.update_prev_and_next_blocks("tail", self.prev_block, None)

        self.assertDictEqual(self.prev_block, {
            "position": "tail",
            "prev_number": "0xc1"
        })

    def test_position_is_mid_and_prev_block_is_none(self):
        with self.assertRaises(ErrorHandler) as ContextManager:
            BlockService.update_prev_and_next_blocks("mid", None, self.next_block)

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "Middle block has no previous or next!")

    def test_position_is_mid_and_next_block_is_none(self):
        with self.assertRaises(ErrorHandler) as ContextManager:
            BlockService.update_prev_and_next_blocks("mid", self.prev_block, None)

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "Middle block has no previous or next!")

    def test_position_is_mid_and_prev_block_is_not_none_and_next_block_is_not_none(self):
        self.prev_block["number"] = "0xc2"
        self.next_block["number"] = "0xc5"

        BlockService.update_prev_and_next_blocks("mid", self.prev_block, self.next_block)

        self.assertEqual(self.prev_block["next_number"], self.next_block["number"])
        self.assertEqual(self.next_block["prev_number"], self.prev_block["number"])


if __name__ == "__main__":
    unittest.main()
