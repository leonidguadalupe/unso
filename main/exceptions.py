from flask import jsonify


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}


BAD_REQUEST = template(['You are missing a query parameter'], code=400)
INCORRECT_FORMAT = template(['Only accept Alphanumeric type inputs'], code=400)
NOT_FOUND = template(['Code not found.'], code=404)


class InvalidTransaction(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def missing_kwargs(cls):
        return cls(**BAD_REQUEST)

    @classmethod
    def incorrect_input_format(cls):
        return cls(**INCORRECT_FORMAT)

    @classmethod
    def input_not_found(cls):
        return cls(**NOT_FOUND)
