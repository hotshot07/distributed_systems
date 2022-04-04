from functools import wraps
from typing import List

import jwt
from flask import make_response, request

ATHLETE = "Athlete"
ORCHESTRATOR = "Orchestrator"
TESTER = "Tester"
WADA = "WADA"
ADMIN = "Admin"
INVALID_TOKEN = "Token is Invalid"
MISSING_TOKEN = "Token is missing"
SECRET_KEYS = {
    "Athlete": "thisisthesecretkeyAthlete",
    "Tester": "thisisthesecretkeyTester",
    "Orchestrator": "thisisthesecretkeyOrchestrator",
    "WADA": "thisisthesecretkeyWADA",
    "Admin": "thisisthesecretkeyADMIN",
}


def decode_token(Users, token):
    for user in Users:
        try:
            data = jwt.decode(token, SECRET_KEYS[user], algorithms=["HS256"])
            if data:
                return user
        except:
            continue


def token_required(Users: List):
    def token(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "X-Access-Token" in request.headers:
                token = request.headers["X-Access-Token"]

            if not token:
                return make_response(MISSING_TOKEN, 401)
            user = decode_token(Users, token)
            try:
                data = jwt.decode(token, SECRET_KEYS[user], algorithms=["HS256"])

            except:
                return make_response(INVALID_TOKEN, 401)

            return f(*args, **kwargs)

        return decorated

    return token
