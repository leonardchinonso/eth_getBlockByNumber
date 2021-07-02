import os
import json
from app import app
from app.services.errorService import ErrorHandler
from app.services import utilService as UtilService
from app.services import blockService as BlockService

app.config["CAPACITY"] = os.getenv("CAPACITY")
CAPACITY = int(app.config["CAPACITY"])

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../models/cache.json")

if CAPACITY <= 1:
    raise ErrorHandler("Capacity cannot be less than 1", status_code=500)


if not os.path.exists(path):
    with open(path, "w"):
        pass


def get_cache():
    cache_file = open(path, "r")

    data = cache_file.read()

    cache_file.close()

    records = {}

    if data:
        records = json.loads(data)

    return records


def write_to_cache_file(cache_data):
    cache_file = open(path, "w")

    json.dump(cache_data, cache_file)

    cache_file.close()


def cache_is_full(cache):
    if len(cache) == CAPACITY:
        return True
    return False


def remove_tail_from_cache(cache):
    tail, prev_block = None, None

    for number, block in cache.items():
        if block["position"] == "tail":
            tail = block

            if "prev_number" in tail:
                prev_block = cache[tail["prev_number"]]

            break

    del cache[tail["number"]]

    if prev_block is not None:
        prev_block["position"] = "tail"
        del prev_block["next_number"]


def remove_block_by_number(number, cache):
    del cache[number]


def add_block_by_number(number, cache, block):
    cache[number] = block


def get_head_from_cache(cache):
    for number, block in cache.items():
        if block["position"] == "head":
            return block
    return None


def add_to_head_of_cache(new_block, latest_block):
    cache = get_cache()

    latest_block_number_decimal = UtilService.convert_hex_to_int(latest_block["number"])
    new_block_number_decimal = UtilService.convert_hex_to_int(new_block["number"])

    if latest_block_number_decimal - new_block_number_decimal <= 20:
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

    BlockService.set_adjacent_block(head, "prev_number", new_block["number"])

    BlockService.set_adjacent_block(new_block, "next_number", head["number"])

    add_block_by_number(new_block["number"], cache, new_block)

    write_to_cache_file(cache)


def remove_block_from_cache(block_to_remove):
    cache = get_cache()

    prev_block = BlockService.get_adjacent_block(block_to_remove, "prev_number", cache)
    next_block = BlockService.get_adjacent_block(block_to_remove, "next_number", cache)

    BlockService.update_prev_and_next_blocks(block_to_remove["position"], prev_block, next_block)

    remove_block_by_number(block_to_remove["number"], cache)

    write_to_cache_file(cache)
