import os
from app.services import utilService as UtilService
from app.models.cache import Cache

CAPACITY = int(os.getenv("CAPACITY"))

cache = Cache(CAPACITY)


def get_cache():
    return cache


def is_within_latest_block(block_number, latest_block_number):
    latest_block_number_decimal = UtilService.convert_hex_to_int(latest_block_number)
    new_block_number_decimal = UtilService.convert_hex_to_int(block_number)

    if 0 <= latest_block_number_decimal - new_block_number_decimal <= 20:
        return True

    return False


# def add_to_head_of_cache(new_block, latest_block, cache):
#     if is_within_latest_block(new_block, latest_block):
#         return
#
#     if len(cache) == 0:
#         BlockService.set_block_position(new_block, "head")
#
#         add_block_by_number(new_block["number"], cache, new_block)
#
#         write_to_cache_file(cache)
#
#         return
#
#     if len(cache) == 5:
#         remove_tail_from_cache(cache)
#
#     head = get_head_from_cache(cache)
#
#     if len(cache) == 1:
#         BlockService.set_block_position(head, "tail")
#     else:
#         BlockService.set_block_position(head, "mid")
#
#     BlockService.set_block_position(new_block, "head")
#
#     BlockService.set_block_field(head, "prev_number", new_block["number"])
#
#     BlockService.set_block_field(new_block, "next_number", head["number"])
#
#     add_block_by_number(new_block["number"], cache, new_block)
#
#     write_to_cache_file(cache)


# def remove_block_from_cache(block_to_remove, cache):
#     prev_block = BlockService.get_adjacent_block(block_to_remove, "prev_number", cache)
#     next_block = BlockService.get_adjacent_block(block_to_remove, "next_number", cache)
#
#     BlockService.update_prev_and_next_blocks(block_to_remove["position"], prev_block, next_block)
#
#     remove_block_by_number(block_to_remove["number"], cache)
#
#     write_to_cache_file(cache)
