from app.services.errorService import ErrorHandler
from app.controllers import blockController as BlockController
from app.services import utilService as UtilService


def get_transaction_by_index(block, index):
    decimal_equivalent = UtilService.convert_hex_to_int(index)
    if "transactions" in block and decimal_equivalent >= len(block["transactions"]):
        new_block = BlockController.get_block_by_number_from_cloud_flare(block["number"])

        if "transactions" in new_block and decimal_equivalent >= len(new_block["transactions"]):
            raise ErrorHandler("Transaction index out of range!", status_code=400)

        BlockController.update_block_in_cache(block["number"], new_block)

        return new_block["transactions"][decimal_equivalent]

    return block["transactions"][decimal_equivalent]


def get_transaction_by_hash_value(block, hash_value):
    for transaction in block["transactions"]:
        if transaction["hash"] == hash_value:
            return transaction

    new_block = BlockController.get_block_by_number_from_cloud_flare(block["number"])

    for transaction in new_block["transactions"]:
        if transaction["hash"] == hash_value:
            BlockController.update_block_in_cache(block["number"], new_block)
            return transaction

    raise ErrorHandler("Cannot retrieve transaction from hash!", status_code=400)


def get_transaction(block_param, txs_param):
    block = BlockController.get_block(block_param)

    if UtilService.is_hash(txs_param):
        return get_transaction_by_hash_value(block, txs_param)

    return get_transaction_by_index(block, txs_param)
