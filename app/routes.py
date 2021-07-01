from flask import Flask, request, jsonify
from app import app
from app.controllers import blockController


@app.route("/blocks/<p>", methods=["GET"])
def get_block(p):
    block = blockController.get_block(p)
    return jsonify({"block": block})
