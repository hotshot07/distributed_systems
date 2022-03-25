from flask import Flask, jsonify, request
from dynamo_handler import *
from models import *
import logging
# logging.basicConfig(level=logging.DEBUG, filename='app.log' ,filemode='w')


app = Flask(__name__)


@app.route("/create-athlete-account", methods=['GET', 'POST'])
def create_athlete_account():
    if request.method == 'POST':
        
        data = request.get_json()
        athlete_model = Athlete(**data)
        
        app.logger.info(f"Recieved create account request for athlete {data}")
        
        ## will return false if any of the required fields are missing
        if not athlete_model.check():
            app.logger.error("Missing required fields")
            return jsonify({"error": "Missing data parameters"}), 400

        return create_user_if_not_exists(**athlete_model.account_dict())


@app.route("/create-orch-account", methods=['GET', 'POST'])
def create_orchestrator_account():
    if request.method == 'POST':
        
        data = request.get_json()
        orchestrator_model = Orchestrator(**data)
        
        app.logger.info(f"Recieved create account request for orchestrator {data}")
        
        ## will return false if any of the required fields are missing
        if not orchestrator_model.check():
            app.logger.error("Missing required fields")
            return jsonify({"error": "Missing or invalid data parameters"}), 400

        return create_user_if_not_exists(**orchestrator_model.account_dict())



@app.route("/create-tester-account", methods=['GET', 'POST'])
def create_tester_account():
    if request.method == 'POST':
        
        data = request.get_json()
        tester_model = Tester(**data)
        
        app.logger.info(f"Recieved create account request for tester {data}")
        
        ## will return false if any of the required fields are missing
        if not tester_model.check():
            app.logger.error("Missing required fields")
            return jsonify({"error": "Missing data parameters"}), 400

        return create_user_if_not_exists(**tester_model.account_dict())


if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(port=5000, debug =True)