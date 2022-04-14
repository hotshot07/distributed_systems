from flask import Flask, jsonify, request
from flask_cors import CORS

from forms import CreateTestForm, UpdateTestResultForm
from dynamodb_handler import (
    update_test_result,
    create_test_using_transaction,
    get_upcoming_tests_for_tester
)
from settings import *
from auth import token_required, WADA, ATHLETE, ORCHESTRATOR, TESTER, ADMIN
import logging

app = Flask(__name__)
CORS_ALLOW_ORIGIN = "*,*"
CORS_EXPOSE_HEADERS = "*,*"
CORS_ALLOW_HEADERS = "content-type,*"
CORS(app, origins=CORS_ALLOW_ORIGIN.split(","),
        allow_headers=CORS_ALLOW_HEADERS.split(","), 
        expose_headers=CORS_EXPOSE_HEADERS.split(","),   
        supports_credentials=True)

@app.route("/assign-athlete-test", methods=['GET', 'POST'])
@token_required([ADMIN, ORCHESTRATOR, WADA])
def assign_test():
    if request.is_json and request.method == 'POST':
        app.logger.info(
            f"Received request to assign a test: {request.get_json()}")
        form = CreateTestForm(athlete_id=request.get_json().get('athlete_id'),
                              date=request.get_json().get('date'),
                              tester_id=request.get_json().get('tester_id'),
                              orchestrator_id=request.get_json().get('orchestrator_id'))
        if form.validate():
            msg, http_code = create_test_using_transaction(athlete_id=form.athlete_id,
                                                           orchestrator_id=form.orchestrator_id,
                                                           date=form.date,
                                                           tester_id=form.tester_id)
            if http_code == 200:
                app.logger.info(f"Item added to test table: {msg}")
                return jsonify({'message': ITEM_ADDED_SUCCESSFULLY, "additonal_info": msg}), http_code
            else:
                app.logger.info(f"Failed to add item to test table: {msg}")
                return jsonify({'message': msg}), http_code
        else:
            return jsonify({"message": ITEM_PARAMETERS_INVALID, "form": form.validation_failures})
    return jsonify({'form': {
        'availability_id': 'str',
        'date': 'str',
        'tester_id': 'str',
        'orchestrator_id': 'str'
    }})


@app.route("/upload-test-result", methods=['GET', 'POST'])
@token_required([ADMIN, ORCHESTRATOR, TESTER])
def upload_test_result():
    if request.method == 'POST' and request.is_json:
        app.logger.info(
            f"Received request to upload a test result: {request.get_json()}")
        form = UpdateTestResultForm(request.get_json().get('test_datetime'), request.get_json(
        ).get('tester_id'), request.get_json().get('test_result'))
        if form.validate():
            response, http_code = update_test_result(
                tester_id=form.tester_id, test_datetime=form.test_datetime, test_result=form.result)
            if http_code == 200:
                app.logger.info(f"Test result uploaded: {response}")
                return jsonify({'message': ITEM_UPDATED_SUCCESSFULLY, 'dynamodb_msg': response}), http_code
            else:
                app.logger.info(f"Failed to upload test result: {response}")
                return jsonify({'message': ITEM_PARAMETERS_INVALID, 'dynamodb_msg': response}), http_code


@app.route("/view-upcoming-tests/<string:tester>", methods=['GET', 'POST'])
@token_required([ADMIN, ORCHESTRATOR, TESTER, WADA])
def view_upcoming_tests(tester: str):
    if tester:
        response, http_code = get_upcoming_tests_for_tester(tester_id=tester)
        if http_code == 200:
            return jsonify({'message': response}), http_code
        else:
            return jsonify({'message': response}), http_code


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Schedule athlete test service is now running!")

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(port=5000, debug=True)
