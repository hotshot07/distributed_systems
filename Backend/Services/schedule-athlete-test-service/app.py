from flask import Flask, jsonify, request

from forms import CreateTestForm, UpdateTestResultForm
from dynamodb_handler import update_test_result, create_test_using_transaction
from settings import *
import logging

app = Flask(__name__)


@app.route("/assign-athlete-test", methods=['GET', 'POST'])
def assign_test():
    if request.is_json and request.method == 'POST':
        form = CreateTestForm(athlete_id=request.get_json().get('athlete_id'),
                              date=request.get_json().get('date'),
                              tester_id=request.get_json().get('tester_id'),
                              orchestrator_id=request.get_json().get('orchestrator_id'))
        if form.validate():
            test_item, dynamo_msg = create_test_using_transaction(athlete_id=form.athlete_id,
                                                orchestrator_id=form.orchestrator_id,
                                                date=form.date,
                                                tester_id=form.tester_id)
            if dynamo_msg == ITEM_COULD_NOT_BE_ADDED:
                return jsonify({'message': ITEM_COULD_NOT_BE_ADDED, "failed_item": test_item}), 400
            elif dynamo_msg == ITEM_PARAMETERS_INVALID:
                return jsonify({'message': ITEM_PARAMETERS_INVALID, "stack_trace": test_item}), 400
            else:
                return jsonify({'message': ITEM_ADDED_SUCCESSFULLY, 'dynamodb_msg': dynamo_msg, 'test_item': test_item}), 201
    return jsonify({'form': {
        'availability_id': 'str',
        'date': 'str',
        'tester_id': 'str',
        'orchestrator_id': 'str'
    }})


@app.route("/upload-test-result", methods=['GET', 'POST'])
def upload_test_result():
    if request.method == 'POST' and request.is_json:
        form = UpdateTestResultForm(request.get_json().get('test_datetime'), request.get_json(
        ).get('tester_id'), request.get_json().get('test_result'))
        if form.validate():
            response, http_code = update_test_result(
                tester_id=form.tester_id, test_datetime=form.test_datetime, test_result=form.result)
            if http_code == 200:
                return jsonify({'message': ITEM_UPDATED_SUCCESSFULLY, 'dynamodb_msg': response}), http_code
            else:
                return jsonify({'message': ITEM_PARAMETERS_INVALID, 'dynamodb_msg': response}), http_code


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Schedule athlete test service is now running!")

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(port=5000, debug=True)
