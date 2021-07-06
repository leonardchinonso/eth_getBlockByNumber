import os
from app.services import utilService as UtilService
from app.models.cache import Cache

from dotenv import load_dotenv

load_dotenv()

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
