import datetime
import logging
import re
from functools import wraps

import jwt
from flask import Flask, jsonify, make_response, request
from werkzeug.security import check_password_hash

from service import query_auth_table, query_user_profile_table

app = Flask(__name__)

app.config["SECRET_KEY"] = "thisisthesecretkey"
TOKEN_EXPIRY_MINUTES = 30


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "X-Access-Token" in request.headers:
            token = request.headers["X-Access-Token"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"message": "Token is invalid"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/unprotected")
def unprotected():
    return jsonify({"message": "Anyone can view this"})


@app.route("/protected")
@token_required
def protected():
    return jsonify({"message": "This is only available if you authenticated"})


@app.route("/login", methods=["POST"])
def login():
    if (
        not request.authorization
        or not request.authorization.username
        or not request.authorization.password
    ):
        return make_response(
            "could not verify", 401, {"Authentication": 'login required"'}
        )

    # Aquire username and password from auth headers
    username = request.authorization.username
    password = request.authorization.password

    username = username.strip()
    # Check if attempted login is with email. Query UserProfiles table for ID if email.
    if is_email(username):
        response = query_user_profile_table(username)

        if response["Count"] == 0:
            return jsonify({"message": "User does not exist!"}), 404

        user_id = response["Items"][0]["Id"]
    else:
        user_id = username

    # Retrieve hashed password from AuthTable for user-id.
    response = query_auth_table(user_id)

    # If no entries in Auth table found, return error.
    if response["Count"] == 0:
        return jsonify({"message": "User does not exist"}), 404

    hashed_password = response["Items"][0]["hashed_password"]

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
        response = make_response("Token returned. User Authenticated.")
        response.headers["X-Access-Token"] = token
        response.set_cookie("Access Token", token)

        return response
    return make_response(
        "Could not verify", 401, {
            "WWW-Authenticate": 'Basic realm="Login Required"'}
    )


# Check if supplied login credential is an email.
def is_email(email_or_id):
    return any(
        re.findall(
            "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email_or_id)
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)

if __name__ != "__main__":
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Authentication service is now running!")
