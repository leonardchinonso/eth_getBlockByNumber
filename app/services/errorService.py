from flask import jsonify, request
from app import app


class ErrorHandler(Exception):
    status_code = 400

    def __init__(self, message: str, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(ErrorHandler)
def handle_error(e):
    return jsonify(e.to_dict())
