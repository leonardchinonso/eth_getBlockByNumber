from app.services.errorService import ErrorHandler


def reset_block(block):
    if "prev_number" in block:
        del block["prev_number"]

    if "next_number" in block:
        del block["next_number"]

    if "position" in block:
        del block["position"]
        
    return block


def get_adjacent_block(block, adjacent_number, cache):
    if adjacent_number in block:
        return cache[block[adjacent_number]]
    return None


def set_adjacent_block(block, adjacent_number, number):
    block[adjacent_number] = number


def update_prev_and_next_blocks(position, prev_block, next_block):
    if position == "head":
        if next_block is not None:
            next_block["position"] = "head"
            del next_block["prev_number"]

    elif position == "tail":
        if prev_block is None:
            raise ErrorHandler("Tail block has no previous")

        if prev_block["position"] != "head":
            prev_block["position"] = "tail"

        del prev_block["next_number"]

    elif position == "mid":
        if prev_block is None or next_block is None:
            raise ErrorHandler("Middle block has no previous or next")

        prev_block["next_number"] = next_block["number"]
        next_block["prev_number"] = prev_block["number"]


def set_block_position(block, position):
    block["position"] = position
