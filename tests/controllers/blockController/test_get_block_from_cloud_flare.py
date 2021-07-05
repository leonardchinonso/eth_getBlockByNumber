import os
import sys
import unittest
import requests
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("BASE_PATH"))

from app.controllers import blockController as BlockController
from app.services.errorService import ErrorHandler


class TestGetBlockFromCloudFlare(unittest.TestCase):

    def setUp(self) -> None:
        self.url = os.getenv("CLOUDFLARE_URL")

    # Cannot test latest because it changes every second
    def test_get_latest_block_from_cloud_flare_successfully(self):
        response = requests.post(self.url, json={
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": ["latest", True],
            "id": 1
        })

        data = response.json()
        self.assertIsNotNone(data)

    def test_get_block_by_number_from_cloud_flare_successfully(self):
        response = requests.post(self.url, json={
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": ["0xc1234", True],
            "id": 1
        })

        response = response.json()
        block = BlockController.get_block_from_cloud_flare("0xc1234")

        self.assertEqual(response["result"], block.data)

    def test_get_block_from_cloud_flare_with_invalid_hex_number(self):
        with self.assertRaises(ErrorHandler) as ContextManager:
            BlockController.get_block_from_cloud_flare("0xc123g")

        exception = ContextManager.exception
        self.assertEqual(exception.status_code, 400)
        self.assertEqual(exception.message, "Invalid argument 0: hex string \"0x\"")

    def test_get_block_from_cloud_flare_returns_none(self):
        self.assertIsNone(BlockController.get_block_from_cloud_flare("0xc123412341234"))


if __name__ == '__main__':
    unittest.main()
