from flask import Flask, request
import random

app = Flask(__name__)

colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'cyan', 'magenta']

@app.route("/color", methods=['GET'])
def index():
    
    return random.choice(colors)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
    