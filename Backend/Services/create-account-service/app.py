from flask import Flask, jsonify, request
from dynamo_handler import *
from models import *

app = Flask(__name__)

# three diffferent routres for different account types
# yes they follow the same pattern, but i wanted separation of concern + if we ever need to update one model,
# we can do it without affecting the other models
@app.route("/create-athlete-account", methods=['GET', 'POST'])
def create_athlete_account():
    if request.method == 'POST':
        
        data = request.get_json()
        athlete_model = Athlete(**data)
        
        ## will return false if any of the required fields are missing
        if not athlete_model.check():
            return jsonify({"error": "Missing data parameters"}), 400

        return create_user_if_not_exists(**athlete_model.account_dict())


@app.route("/create-orch-account", methods=['GET', 'POST'])
def create_orchestrator_account():
    if request.method == 'POST':
        
        data = request.get_json()
        orchestrator_model = Orchestrator(**data)
        
        ## will return false if any of the required fields are missing
        if not orchestrator_model.check():
            return jsonify({"error": "Missing or invalid data parameters"}), 400

        return create_user_if_not_exists(**orchestrator_model.account_dict())



@app.route("/create-tester-account", methods=['GET', 'POST'])
def create_tester_account():
    if request.method == 'POST':
        
        data = request.get_json()
        tester_model = Tester(**data)
        
        ## will return false if any of the required fields are missing
        if not tester_model.check():
            return jsonify({"error": "Missing data parameters"}), 400

        return create_user_if_not_exists(**tester_model.account_dict())


if __name__ == "__main__":
    app.run(port=5000, debug =True)