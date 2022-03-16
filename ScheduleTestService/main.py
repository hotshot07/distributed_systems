from flask import Flask, jsonify, request
import requests
from forms import CreateTestForm
from dynamodb_handler import create_test
from constants import *

app = Flask(__name__)


@app.route("/assign-athlete-test", methods=['GET', 'POST'])
def assign_test():
    if request.is_json:
        form = CreateTestForm(request.get_json().get('availability_id'),
                            request.get_json().get('tester_id'),
                            request.get_json().get('orchestrator_id'))
    if request.method == 'POST' and form.validate():
        test_item, dynamo_msg = create_test(availability_id=form.availability_id,
                                            orchestrator_id=form.orchestrator_id,
                                            tester_id=form.tester_id)
        if dynamo_msg == ITEM_ALREADY_EXISTS:
            return jsonify({'message': ITEM_ALREADY_EXISTS}), 400
        else:
            return jsonify({'message': ITEM_ADDED_SUCCESSFULLY, 'dynamodb_msg': dynamo_msg, 'test_item': test_item}), 201
    return jsonify({'form': {
        'availability_id' : 'str',
        'tester_id' : 'str',
        'orchestrator_id' : 'str'
    }})

# TODO
@app.route("/upload-test-result", methods=['GET', 'POST'])
def upload_test_result():
    ...

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
