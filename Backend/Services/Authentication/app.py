import datetime
from functools import wraps
from pprint import pprint

import boto3
import flask
import jwt
from boto3.dynamodb.conditions import Key
from flask import Flask, jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "thisisthesecretkey"
AUTH = "Auth"
USER_PROFILE = "UserProfile"
AWS_ACCESS_KEY_ID = "AKIAZN3M6N6WYMZ2TGMF"
AWS_SECRET_ACCESS_KEY = "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"
REGION_NAME = "eu-west-1"

resource = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


AuthTable = resource.Table(AUTH)
UserProfileTable = resource.Table(USER_PROFILE)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        print(request)
        print(flask.request.headers.get("x-access-tokens"))
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]
        print(token)

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
    return jsonify({"message": "This is only available if you authenticate"})


@app.route("/login/<username>/<password>")
def login(username, password):

    # id from req
    # Get id and hashed password from dyn
    # If returned object is populated cnt
    # else throw return error

    # Hash the password that came in as req
    # check if hashed_pass from dyn == hash(pass_from_request)
    response = UserProfileTable.query(
        IndexName="Email-index", KeyConditionExpression=Key("Email").eq(username)
    )

    if response["Count"] == 0:
        return jsonify({"message": "User does not exist"}), 404

    user_id = response["Items"][0]["Id"]
    pprint(user_id)

    response = AuthTable.query(
        IndexName="userid-index", KeyConditionExpression=Key("userid").eq(user_id)
    )
    pprint(response["Items"][0]["hashed_password"])

    if check_password_hash(response["Items"][0]["hashed_password"], password):

        token = jwt.encode(
            {
                "user": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )
        pprint(token)
        response = make_response("hello")
        response.headers["x-access-tokens"] = token
        print(response.headers)
        return response
    return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})


if __name__ == "__main__":
    app.run(debug=True)
