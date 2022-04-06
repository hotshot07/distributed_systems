import datetime
from distutils.command.build import build
import logging
import re
from functools import wraps
from typing import List

import jwt
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from werkzeug.security import check_password_hash

from service import (
    query_auth_table,
    query_user_profile_table_email,
    query_user_profile_table_id,
)
from settings import (
    ATHLETE,
    COULD_NOT_VERIFY,
    INVALID_TOKEN,
    MISSING_TOKEN,
    ORCHESTRATOR,
    SECRET_KEYS,
    TESTER,
    TOKEN_EXPIRY_MINUTES,
    USER_AUTHENTICATED,
    USER_DOES_NOT_EXIST,
    WADA,
    ADMIN,
)

app = Flask(__name__)
CORS_ALLOW_ORIGIN = "*,*"
CORS_EXPOSE_HEADERS = "*,*"
CORS_ALLOW_HEADERS = "content-type,*"
CORS(app, origins=CORS_ALLOW_ORIGIN.split(","),
        allow_headers=CORS_ALLOW_HEADERS.split(","), 
        expose_headers=CORS_EXPOSE_HEADERS.split(","),   
        supports_credentials=True)

app.config["SECRET_KEY"] = SECRET_KEYS #


def decode_token(Users, token):
    for user in Users:
        try:
            data = jwt.decode(
                token, app.config["SECRET_KEY"][user], algorithms=["HS256"]
            )
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
                data = jwt.decode(
                    token, app.config["SECRET_KEY"][user], algorithms=["HS256"]
                )

            except:
                return make_response(INVALID_TOKEN, 401)

            return f(*args, **kwargs)

        return decorated

    return token


@app.route("/unprotected")
def unprotected():
    return jsonify({"message": "Anyone can view this"})


@app.route("/protected")
@token_required([ATHLETE, TESTER, ADMIN, ORCHESTRATOR, WADA])
def protected():
    return jsonify({"message": "This is only available if you authenticated"})


@app.route("/login", methods=["POST", "OPTIONS"])
def login():
    print(request)
    if (request.method == "OPTIONS"):
        return build_preflight_response(), 200

    elif (request.method == "POST"):
        if (
            not request.authorization
            or not request.authorization.username
            or not request.authorization.password
        ):
            print(request.__dict__)
            return make_response(
                COULD_NOT_VERIFY, 401, {"Authentication": 'login required"'}
            )
        # Aquire username and password from auth headers
        username = request.authorization.username
        password = request.authorization.password
        print(request.__dict__)
        username = username.strip()
        # Check if attempted login is with email. Query UserProfiles table for ID if email.
        if is_email(username):
            user_profile_response = query_user_profile_table_email(username)

            if user_profile_response["Count"] == 0:
                return make_response(USER_DOES_NOT_EXIST, 404)

            user_id = user_profile_response["Items"][0]["Id"]
        else:
            user_id = username

        # Retrieve hashed password from AuthTable for user-id.
        auth_table_response = query_auth_table(user_id)

        # If no entries in Auth table found, return error.
        if auth_table_response["Count"] == 0:
            return make_response(USER_DOES_NOT_EXIST, 404)

        hashed_password = auth_table_response["Items"][0]["hashed_password"]

        # Check the password hash vs the password from the auth headers.
        if check_password_hash(hashed_password, password):
            token = jwt.encode(
                {
                    "user": username,
                    "exp": datetime.datetime.utcnow()
                    + datetime.timedelta(minutes=TOKEN_EXPIRY_MINUTES),
                },
                app.config["SECRET_KEY"],
            )
            # Create the response with the JWT in both cookies and X-Access-Token header.
            response = make_response(token)
            response.headers.add('Access-Control-Allow-Headers', "*")
            response.headers.add('Access-Control-Allow-Methods', "*")
            response.headers.add("Access-Control-Allow-Origin", "*")

            return response, 200
        return make_response(
            COULD_NOT_VERIFY, 401, {
                "WWW-Authenticate": 'Basic realm="Login Required"'}
        )
        # Create the response with the JWT in both cookies and X-Access-Token header.
        response = make_response(f"{USER_AUTHENTICATED} >> {account_type}")
        response.headers["X-Access-Token"] = token
        response.set_cookie("Access Token", token)

        return response
    return make_response(
        COULD_NOT_VERIFY, 401, {
            "WWW-Authenticate": 'Basic realm="Login Required"'}
    )


# Check if supplied login credential is an email.
def is_email(email_or_id):
    return any(
        re.findall(
            "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email_or_id)
    )


def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)

if __name__ != "__main__":
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Authentication service is now running!")
