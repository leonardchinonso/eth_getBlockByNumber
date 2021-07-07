from app.services.errorService import ErrorHandler
from app.controllers import blockController as BlockController
from app.services import utilService as UtilService


def get_transaction_by_index(data: dict, index: str) -> dict:
    decimal_equivalent = UtilService.convert_hex_to_int(index)

    if decimal_equivalent >= len(data["transactions"]):
        raise ErrorHandler("Transaction index out of range!", status_code=400)

    return data["transactions"][decimal_equivalent]


def get_transaction_by_hash_value(data: dict, hash_value: str) -> dict:
    for transaction in data["transactions"]:
        if transaction["hash"] == hash_value:
            return transaction

    raise ErrorHandler("Cannot retrieve transaction from hash!", status_code=400)


def get_transaction(block_param: str, txs_param: str) -> dict:
    block = BlockController.get_block(block_param)

    if UtilService.is_hash(txs_param):
        return get_transaction_by_hash_value(block.data, txs_param)

    return get_transaction_by_index(block.data, txs_param)
