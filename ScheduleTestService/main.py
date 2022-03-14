from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return jsonify({'msg': 'this is a test message'})


if __name__ == "__main__":
    app.run( host="0.0.0.0", port=5000)