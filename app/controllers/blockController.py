import json
import os.path
from app.services.errorService import ErrorHandler


def get_cache():
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../models/cache.json")

    cache_file = open(path, "r")
    data = cache_file.read()
    cache_file.close()

    records = json.loads(data)
    print(records)
    return records


def get_head_from_cache():
    cache = get_cache()
    for id, block in cache.items():
        if block["position"] == "head":
            return block
    return None


def get_tail_from_cache():
    cache = get_cache()
    for id, block in cache.items():
        if block["position"] == "tail":
            return block
    return None


def get_block_by_number(block_number):
    cache = get_cache()
    for id, block in cache.items():
        if str(block_number) == id:
            return block
    return None


def get_block(block_param):
    if block_param == "latest":
        block = get_head_from_cache()
    else:
        block = get_block_by_number(block_param)
    if block is None:
        raise ErrorHandler("Block not found!", status_code=404)
    return block



