from flask import Flask, jsonify, request
from dynamo_handler import *
from models import *
import logging
# logging.basicConfig(level=logging.DEBUG, filename='app.log' ,filemode='w')


app = Flask(__name__)

# three diffferent routres for different account types
# yes they follow the same pattern, but i wanted separation of concern + if we ever need to update one model,
# we can do it without affecting the other models
@app.route("/create-athlete-account", methods=['GET', 'POST'])
def create_athlete_account():
    if request.method == 'POST':
        
        app.logger.debug("I'm a DEBUG message")
        app.logger.info("I'm an INFO message")
        app.logger.warning("I'm a WARNING message")
        app.logger.error("I'm a ERROR message")
        app.logger.critical("I'm a CRITICAL message")
        
        data = request.get_json()
        athlete_model = Athlete(**data)
        
        ## will return false if any of the required fields are missing
        if not athlete_model.check():
            app.logger.debug("Missing required fields")
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


if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.debug')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.debug("I'm a DEBUG message")

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug("I'm a DEBUG message")
    app.run(port=5000, debug =True)