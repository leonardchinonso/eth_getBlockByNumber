from flask import Flask, request, jsonify, make_response
from app import app
from app.controllers import blockController as BlockController
from app.controllers import transactionController as TransactionController


@app.route("/block/<block_param>", methods=["GET"])
def get_block(block_param):
    block = BlockController.get_block(block_param)

    return make_response(jsonify({"status_code": 200, "data": block}))


@app.route("/block/<block_param>/txs/<txs_param>", methods=["GET"])
def get_transaction(block_param, txs_param):
    transaction = TransactionController.get_transaction(block_param, txs_param)

    return make_response(jsonify({"status_code": 200, "data": transaction}))
