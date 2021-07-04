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
        if block[adjacent_number] in cache:
            return cache[block[adjacent_number]]
        raise ErrorHandler("Cannot get adjacent cache!", 400, block)
    return None


def set_block_field(block, field, value):
    block[field] = value


def update_prev_and_next_blocks(position, prev_block, next_block):
    if position == "head":
        if next_block is not None:
            set_block_position(next_block, "head")
            del next_block["prev_number"]

    elif position == "tail":
        if prev_block is None:
            raise ErrorHandler("Tail block has no previous!")

        elif prev_block["position"] != "head":
            set_block_position(prev_block, "tail")

        del prev_block["next_number"]

    elif position == "mid":
        if prev_block is None or next_block is None:
            raise ErrorHandler("Middle block has no previous or next!")

        set_block_field(prev_block, "next_number", next_block["number"])
        set_block_field(next_block, "prev_number", prev_block["number"])


def set_block_position(block, position):
    block["position"] = position
