from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        
        try:
            get_me_a_color = requests.get('http://random-color-service:5000/color')
        except requests.exceptions.ConnectionError:
            return jsonify({"error": "Could not connect to the random-color-service"})
        
        return jsonify({'color': get_me_a_color.text})


if __name__ == "__main__":
    app.run( host="0.0.0.0", port=5000)