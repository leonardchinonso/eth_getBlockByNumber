import os
import json
from app.services.errorService import ErrorHandler
from app.services import utilService as UtilService
from app.services import blockService as BlockService

CAPACITY = int(os.getenv("CAPACITY"))
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../models/cache.json")

if CAPACITY <= 1:
    raise ErrorHandler("Capacity cannot be less than 1", status_code=500)


if not os.path.exists(path):
    with open(path, "w"):
        pass


def get_cache():
    try:
        cache_file = open(path, "r")
    except FileNotFoundError:
        raise ErrorHandler("File for cache does not exist!", 500)

    data = cache_file.read()

    cache_file.close()

    records = {}

    if data:
        records = json.loads(data)

    return records


def write_to_cache_file(cache_data):
    try:
        cache_file = open(path, "w")
    except FileNotFoundError:
        raise ErrorHandler("File for cache does not exist!", 500)

    json.dump(cache_data, cache_file)

    cache_file.close()


def cache_is_full(cache):
    if len(cache) == CAPACITY:
        return True
    return False


def remove_tail_from_cache(cache):
    if len(cache) <= 1:
        return

    tail, prev_block = None, None

    for number, block in cache.items():
        if block["position"] == "tail":
            tail = block

            if "prev_number" in tail:
                prev_block = cache[tail["prev_number"]]
            else:
                raise ErrorHandler("Tail has no previous block!", 500)

            break

    if tail is None:
        raise ErrorHandler("Cache has no tail!", 500)

    del cache[tail["number"]]
    del prev_block["next_number"]

    prev_block["position"] = "tail"


def remove_block_by_number(number, cache):
    del cache[number]


def add_block_by_number(number, cache, block):
    cache[number] = block


def get_head_from_cache(cache):
    for number, block in cache.items():
        if block["position"] == "head":
            return block
    return None


def is_within_latest_block(block, latest_block):
    latest_block_number_decimal = UtilService.convert_hex_to_int(latest_block["number"])
    new_block_number_decimal = UtilService.convert_hex_to_int(block["number"])

    if 0 <= latest_block_number_decimal - new_block_number_decimal <= 20:
        return True

    return False


def add_to_head_of_cache(new_block, latest_block, cache):
    if is_within_latest_block(new_block, latest_block):
        return

    if len(cache) == 0:
        BlockService.set_block_position(new_block, "head")

        add_block_by_number(new_block["number"], cache, new_block)

        write_to_cache_file(cache)

        return

    if cache_is_full(cache):
        remove_tail_from_cache(cache)

    head = get_head_from_cache(cache)

    if len(cache) == 1:
        BlockService.set_block_position(head, "tail")
    else:
        BlockService.set_block_position(head, "mid")

    BlockService.set_block_position(new_block, "head")

    BlockService.set_block_field(head, "prev_number", new_block["number"])

    BlockService.set_block_field(new_block, "next_number", head["number"])

    add_block_by_number(new_block["number"], cache, new_block)

    write_to_cache_file(cache)


def remove_block_from_cache(block_to_remove, cache):
    prev_block = BlockService.get_adjacent_block(block_to_remove, "prev_number", cache)
    next_block = BlockService.get_adjacent_block(block_to_remove, "next_number", cache)

    BlockService.update_prev_and_next_blocks(block_to_remove["position"], prev_block, next_block)

    remove_block_by_number(block_to_remove["number"], cache)

    write_to_cache_file(cache)
