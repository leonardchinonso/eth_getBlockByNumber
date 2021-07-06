import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.getenv("BASE_PATH"))

from app import app


class TestRoutes(unittest.TestCase):

    def test_get_cache(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_latest_block_route(self):
        tester = app.test_client(self)
        response = tester.get("/block/latest", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_block_by_number_route(self):
        tester = app.test_client(self)
        response = tester.get("/block/0x1234", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_transaction_by_index_route(self):
        tester = app.test_client(self)
        response = tester.get("/block/0xc2b16e/txs/0x1", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_transaction_by_hash_value_route(self):
        tester = app.test_client(self)
        response = tester.get("/block/0xc2b16e/txs/0x992c18ba9c25cdc6fa030696fd21e333d33f96a66b509788b5902ded739c5ddd", content_type="application/json")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
