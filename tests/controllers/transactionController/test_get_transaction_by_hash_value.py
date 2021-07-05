import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.models.block import Block
from app.services.errorService import ErrorHandler
from app.controllers import transactionController as TransactionController


class TestGetTransactionByIndex(unittest.TestCase):

    def setUp(self) -> None:
        self.block = Block("0x1234", {
            "number": "0x1234",
            "transactions": [
                {"hash": "0x637117129e873be6ee8ceb088c013fdc05383613c2d4373b4a523bc8a77e2656", "index": "0x0"},
                {"hash": "0x992c18ba9c25cdc6fa030696fd21e333d33f96a66b509788b5902ded739c5ddd", "index": "0x1"},
                {"hash": "0x228e82c24b4bf71ace0e56ddb4f7aa045b04b840bf4c179673d5508f0c872e8d", "index": "0x2"},
            ]
        })

    def test_get_transaction_by_index_raises_exception(self):
        transaction = TransactionController.get_transaction_by_hash_value(self.block.data, "0x228e82c24b4bf71ace0e56ddb4f7aa045b04b840bf4c179673d5508f0c872e8d")
        self.assertEqual(transaction, self.block.data["transactions"][2])

    def test_get_transaction_by_index_returns_valid_transaction(self):
        with self.assertRaises(ErrorHandler) as ContextManager:
            TransactionController.get_transaction_by_hash_value(self.block.data, "0x128e82c24b4bf71ace0e56ddb3e7aa045b04b840bf4c179673d5508f0c872e83")

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "Cannot retrieve transaction from hash!")


if __name__ == '__main__':
    unittest.main()
