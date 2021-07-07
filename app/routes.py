from flask import Flask, request, jsonify, make_response
from app import app
from app.services import cacheService as CacheService
from app.controllers import blockController as BlockController
from app.controllers import transactionController as TransactionController


@app.route("/block/<block_param>", methods=["GET"])
def get_block(block_param: str):
    block = BlockController.get_block(block_param)

    return make_response(jsonify({"status_code": 200, "data": block.data}))


@app.route("/block/<block_param>/txs/<txs_param>", methods=["GET"])
def get_transaction(block_param: str, txs_param: str):
    transaction = TransactionController.get_transaction(block_param, txs_param)

    return make_response(jsonify({"status_code": 200, "data": transaction}))


@app.route("/", methods=["GET"])
def get_cache():
    cache = CacheService.get_cache()

    return make_response(jsonify({"status_code": 200, "data": cache.data}))


@app.route("/tests", methods=["GET"])
def run_tests():
    from app import tests
    return make_response(jsonify({"status_code": 200, "message": "All tests have been run, check your console for logs..."}))
