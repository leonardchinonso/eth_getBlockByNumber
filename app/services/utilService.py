def convert_hex_to_int(hex_number):
    return int(hex_number, 16)


def is_hash(string):
    if len(string) > 10:
        return True
    return False
