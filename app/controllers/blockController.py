import os
import requests
from app import app
from app.services.errorService import ErrorHandler
from app.services import cacheService as CacheService
from app.services import blockService as BlockService


CLOUDFLARE_URL = os.getenv("CLOUDFLARE_URL")


def get_block_by_number_from_cache(block_number, cache):
    if block_number in cache:
        return cache[block_number]

    return None


def get_block_from_cloud_flare(param):
    body = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [param, True],
        "id": 1
    }

    res = requests.post(CLOUDFLARE_URL, json=body)

    data = res.json()

    if "error" in data:
        if data["error"]["code"] == -32602:
            raise ErrorHandler("Invalid argument 0: hex string \"0x\"", status_code=400)

        return None

    return data["result"]


def get_block_by_number(block_number):
    cache = CacheService.get_cache()

    block = get_block_by_number_from_cache(block_number, cache)

    if block is None:
        try:
            block = get_block_from_cloud_flare(block_number)
        except Exception as e:
            raise ErrorHandler(e)

        if block is None:
            return None

    else:
        CacheService.remove_block_from_cache(block, cache)

        block = BlockService.reset_block(block)

    latest_block = get_block("latest")

    CacheService.add_to_head_of_cache(block, latest_block, cache)

    return block


def get_block(block_param):
    if block_param == "latest":
        try:
            block = get_block_from_cloud_flare("latest")
        except Exception as e:
            raise ErrorHandler(e)

        if block is None:
            raise ErrorHandler("Block not found!", status_code=404)

    block = get_block_by_number(block_param)

    if block is None:
        raise ErrorHandler("Block not found!", status_code=404)

    return block
