import os
import requests
from typing import Optional
from app.models.block import Block
from app.services.errorService import ErrorHandler
from app.services import cacheService as CacheService


CLOUDFLARE_URL = os.getenv("CLOUDFLARE_URL")


def get_block_from_cloud_flare(param: str) -> Optional[Block]:
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

    result = data["result"]

    if result is None:
        return None

    return Block(result["number"], result)


def get_block_by_number(block_number: str) -> Optional[Block]:
    cache = CacheService.get_cache()

    block = cache.get_block_by_number(block_number)

    if block is None:
        try:
            block = get_block_from_cloud_flare(block_number)
        except Exception:
            raise ErrorHandler("Cannot get block, please check your connection...")

        if block is None:
            return None

    else:
        cache.remove_block(block)

    latest_block = get_block("latest")

    if not CacheService.is_within_latest_block(block.number, latest_block.number):
        cache.add_to_head(block)

    return block


def get_block(block_param: str) -> Optional[Block]:
    if block_param == "latest":
        try:
            block = get_block_from_cloud_flare("latest")
        except Exception:
            raise ErrorHandler("Cannot get latest block, please check your connection...")

        if block is None:
            raise ErrorHandler("Block not found!", status_code=404)

    else:
        block = get_block_by_number(block_param)

    if block is None:
        raise ErrorHandler("Block not found!", status_code=404)

    return block
