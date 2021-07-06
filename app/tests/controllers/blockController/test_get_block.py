import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.getenv("BASE_PATH"))

from app.services.errorService import ErrorHandler
from app.controllers import blockController as BlockController


class TestGetBlock(unittest.TestCase):

    def test_get_latest_block_returns_valid_block(self):
        data = BlockController.get_block("latest")
        self.assertIsNotNone(data)
        self.assertIsNotNone(data.number)

    def test_get_block_by_number_raises_exception(self):
        with self.assertRaises(ErrorHandler) as ContextManager:
            BlockController.get_block("0x123412341234")

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 404)
        self.assertEqual(exception.message, "Block not found!")


if __name__ == '__main__':
    unittest.main()
