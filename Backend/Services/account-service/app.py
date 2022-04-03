from flask import Flask, jsonify, request
from dynamo_handler import *
from models import *
import logging
from utils import get_id_and_passwords, error_message
from auth import *

app = Flask(__name__)

###
# update routes UPDATE an existing inactive account in user_profile
# create routes CREATE a new inactive account in auth + user_profile
###


@app.route("/", methods=["GET"])
def index():
    return "account-service works"


@app.route("/update-athlete-account", methods=["GET", "POST"])
@token_required([ATHLETE])
def create_athlete_account():
    if request.method == "POST":

        data = request.get_json()
        athlete_model = Athlete(**data)

        app.logger.info(f"Recieved update account request for athlete {data}")

        # will return false if any of the required fields are missing
        if not athlete_model.check():
            app.logger.error("Missing required fields")
            return jsonify(error_message("Missing data parameters")), 400

        return update_user_if_exists(**athlete_model.account_dict())


@app.route("/update-orch-account", methods=["GET", "POST"])
@token_required([ORCHESTRATOR])
def create_orchestrator_account():
    if request.method == "POST":

        data = request.get_json()
        orchestrator_model = Orchestrator(**data)

        app.logger.info(
            f"Recieved update account request for orchestrator {data}")

        # will return false if any of the required fields are missing
        if not orchestrator_model.check():
            app.logger.error("Missing required fields")
            return jsonify(error_message("Missing or invalid data parameters")), 400

        return update_user_if_exists(**orchestrator_model.account_dict())


@app.route("/update-tester-account", methods=["GET", "POST"])
@token_required([TESTER])
def create_tester_account():
    if request.method == "POST":

        data = request.get_json()
        tester_model = Tester(**data)

        app.logger.info(f"Recieved update account request for tester {data}")

        # will return false if any of the required fields are missing
        if not tester_model.check():
            app.logger.error("Missing required fields")
            return jsonify(error_message("Missing data parameters")), 400

        return update_user_if_exists(**tester_model.account_dict())

# helps create admin inactive accounts in auth and user profile
# returns list 
@app.route("/admin-inactive-accounts", methods=["GET", "POST"])
@token_required([ADMIN])
def admin_inactive_accounts():
    if request.method == "POST":
        data = request.get_json()

        country = data.get("Country")
        account_type = data.get("AccountType")

        app.logger.info(f"Recieved request to create account {data}")

        if account_type not in ADMIN_ALLOWED_ACCOUNTS:
            return jsonify(error_message("Invalid account type")), 400

        if not country or not account_type:
            return jsonify(error_message("Missing data parameters")), 400

        
        organization = check_country(country)
        
        if not organization:
            return jsonify(error_message("Invalid country")), 400

        #all checks passed!
        id_password_list = get_id_and_passwords(1)

        account = id_password_list[0]

        current_request = create_inactive_account(
            account, account_type, organization)

        if current_request.status_code != 200:
            return jsonify(error_message("Could not create account")), 400

        #too keep the same format as down below
        return jsonify(id_password_list), 200


@app.route("/create-n-accounts", methods=["GET", "POST"])
#@token_required([ORCHESTRATOR])
def get_n_accounts():
    if request.method == "POST":
        data = request.get_json()

        user_id = data.get("Id")
        organization = data.get("Organization")
        number_of_accounts = data.get("NumberOfAccounts")
        account_type = data.get("AccountType")

        app.logger.info(
            f"Recieved request to create {number_of_accounts} accounts by ID {user_id}"
        )

        if not check_id(user_id, organization):
            return jsonify(error_message("Invalid User ID or Organization")), 400

        id_password_list = get_id_and_passwords(number_of_accounts)

        # store it in auth table + create inactive profiles

        accounts_created = []

        for item in id_password_list:
            current_request = create_inactive_account(
                item, account_type, organization)
            if current_request.status_code != 200:
                app.logger.error(f"Failed to create account for {item}")
                return jsonify(error_message("Failed to create all accounts")), 400
            else:
                accounts_created.append(item)
        return jsonify(accounts_created), 200



if __name__ != "__main__":
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Create account service is now running!")

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host="0.0.0.0", port=5432, debug=True)



#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiOTAxNzYyNDYxMDYiLCJleHAiOjE2NDkwMDQ0MDN9.9U5kqicE0sEWRJCcTSeWT1DmZejqRkAYchYzqXe6OEU