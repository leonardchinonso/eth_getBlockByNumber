from app.services.errorService import ErrorHandler


def convert_hex_to_int(hex_number):
    try:
        decimal_value = int(hex_number, 16)
    except ValueError:
        raise ErrorHandler("Invalid hexadecimal number!", status_code=400)

    return decimal_value


def is_hash(string):
    if len(string) > 10:
        return True
    return False
