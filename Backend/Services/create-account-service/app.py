from flask import Flask, jsonify, request
from dynamo_handler import *
from models import *
import logging
from utils import get_id_and_passowrds

app = Flask(__name__)

# fore external + internal requests
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


# this account type is for internal requests only (IT admin)
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

# this account type is for internal requests only (it admin == us)
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

# will create n number of athlete accounts, to be used by the orchestrator
# expecting orchestrator id and number of accounts to create in JSON
# {
#     "Id": "68011495473",
#     "Organization": "Canada ADO",
#     "NumberOfAccounts": 5,
#     "AccountType": "Athlete"
# }
# orchestrator can create accounts for tester or athlete (Specify account type in JSON)) 
@app.route("/create-n-accounts", methods=['POST'])
def get_n_accounts():
    if request.method == 'POST':
        data = request.get_json()
        
        user_id = data.get('Id')
        organization = data.get('Organization')
        number_of_accounts = data.get('NumberOfAccounts')
        account_type = data.get('AccountType')
        
        app.logger.info(f"Recieved request to create {number_of_accounts} accounts by ID {user_id}")
        
        if not check_id(user_id, organization):
            return jsonify({"error": "Invalid user ID or organization"}), 400 
        
        
        # create_inactive_athelete_accounts(get_id_and_passowrds(number_of_accounts), data['AccountType'])
        
        return jsonify("hi")
        



if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Create account service is now running!")

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(port=5000, debug =True)