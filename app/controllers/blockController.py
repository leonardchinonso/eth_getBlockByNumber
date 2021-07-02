import json
import os
import requests
from app import app
from app.services.errorService import ErrorHandler
from app.services import utilService as UtilService


app.config["CLOUDFLARE_URL"] = os.getenv("CLOUDFLARE_URL")
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


def write_to_cache(cache_data):
    cache_file = open(path, "w")

    json.dump(cache_data, cache_file)

    cache_file.close()


def get_head_from_cache():
    cache = get_cache()

    for number, block in cache.items():
        if block["position"] == "head":
            return block

    return None


def get_tail_from_cache():
    cache = get_cache()

    for number, block in cache.items():
        if block["position"] == "tail":
            return block

    return None


def get_block_by_number_from_cache(block_number):
    cache = get_cache()

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

    res = requests.post(app.config["CLOUDFLARE_URL"], json=body)

    data = res.json()

    if "error" in data:
        if data["error"]["code"] == -32602:
            raise ErrorHandler("invalid argument 0: hex string \"0x\"", status_code=400)

        return None

    return data["result"]


def remove_block_from_cache(block_to_remove):
    cache = get_cache()
    
    prev_block, next_block = None, None

    if "prev_number" in block_to_remove:
        prev_block = cache[block_to_remove["prev_number"]]

    if "next_number" in block_to_remove:
        next_block = cache[block_to_remove["next_number"]]

    if block_to_remove["position"] == "head":
        if next_block is not None:
            next_block["position"] = "head"
            del next_block["prev_number"]

    elif block_to_remove["position"] == "tail":
        if prev_block is None:
            raise ErrorHandler("Tail block has no previous", status_code=404)

        if prev_block["position"] != "head":
            prev_block["position"] = "tail"

        del prev_block["next_number"]

    elif block_to_remove["position"] == "mid":
        if prev_block is None or next_block is None:
            raise ErrorHandler("Middle block has no previous or next", status_code=404)

        prev_block["next_number"] = next_block["number"]
        next_block["prev_number"] = prev_block["number"]

    del cache[block_to_remove["number"]]

    write_to_cache(cache)


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


def add_to_head_of_cache(new_block):
    cache = get_cache()

    latest_block = get_block("latest")

    latest_block_number_decimal = UtilService.convert_hex_to_int(latest_block["number"])
    new_block_number_decimal = UtilService.convert_hex_to_int(new_block["number"])

    if latest_block_number_decimal - new_block_number_decimal <= 20:
        return

    if len(cache) == 0:
        new_block["position"] = "head"

        cache[new_block["number"]] = new_block

        write_to_cache(cache)

        return
    
    if len(cache) == CAPACITY:
        remove_tail_from_cache(cache)

    head = None

    for number, block in cache.items():
        if block["position"] == "head":
            head = block
            break
            
    if len(cache) == 1:
        head["position"] = "tail"
    else:
        head["position"] = "mid"
    
    new_block["position"] = "head"

    head["prev_number"] = new_block["number"]

    new_block["next_number"] = head["number"]

    cache[new_block["number"]] = new_block

    write_to_cache(cache)


def get_block_by_number(block_number):
    block = get_block_by_number_from_cache(block_number)

    if block is None:
        block = get_block_from_cloud_flare(block_number)

        if block is None:
            return None

    else:
        remove_block_from_cache(block)

        if "prev_number" in block:
            del block["prev_number"]

        if "next_number" in block:
            del block["next_number"]

        if "position" in block:
            del block["position"]

    add_to_head_of_cache(block)

    return block


def get_block(block_param):
    print(len(get_cache()))
    if block_param == "latest":
        return get_block_from_cloud_flare("latest")

    block = get_block_by_number(block_param)

    if block is None:
        raise ErrorHandler("Block not found!", status_code=404)

    return block
