from flask import Flask, jsonify, request
from dynamo_handler import *
from models import *
import logging
from utils import get_id_and_passwords
from countries import country_set

app = Flask(__name__)

# fore external + internal requests
@app.route("/update-athlete-account", methods=['GET', 'POST'])
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
@app.route("/update-orch-account", methods=['GET', 'POST'])
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
@app.route("/update-tester-account", methods=['GET', 'POST'])
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



# {
#     "Organization": "Ireland ADO",
#     "AccountType": "Orchestrator",
# }
@app.route("/admin-inactive-accounts", methods=['POST'])
def admin_inactive_accounts():
    if request.method == 'POST':
        data = request.get_json()
        
        organization = data.get('Organization')
        account_type = data.get('AccountType')
        
        app.logger.info(f"Recieved request to create account {data}")
        
        if not organization or not account_type:
            return jsonify({"error": "Missing data parameters"}), 400
        
        country = organization.replace('ADO', '')
        
        if country not in country_set:
            return jsonify({"error": "Invalid organization"}), 400
        
        
        
        
        
        
        
        







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
            return jsonify({"error": "Invalid User ID or Organization"}), 400 
        
        id_password_list = get_id_and_passwords(number_of_accounts)
        
        # store it in auth table + create inactive profiles
        
        accounts_created = []
        
        for item in id_password_list:
            current_request = create_inactive_account(item, account_type, organization)
            if current_request.status_code != 200:
                app.logger.error(f"Failed to create account for {item}")
                return jsonify({"error": "Failed to create all accounts"}), 400
            else:
                accounts_created.append(item)
        
        return jsonify(accounts_created), 200









if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Create account service is now running!")

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(port=5000, debug =True)