from flask import Flask, jsonify, request
import requests


app = Flask(__name__)


@app.route("/create-athlete-account", methods=['GET', 'POST'])
def create_athlete_account():
    if request.method == 'POST':
        data = request.get_json()
        # url = "http://localhost:5000/create-athlete-account"
        # response = requests.post(url, json=data)
        # return jsonify(response.json())
    else:
        return jsonify({"error": "Method not allowed"})


@app.route("/create-ado-account", methods=['GET', 'POST'])
# pass the ado name and email to this account, passoword is created in the db 

@app.route("/create-tester-account", methods=['GET', 'POST'])
# pass the tester name and email to this account, passoword is created


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)