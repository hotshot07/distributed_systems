from flask import Flask, request, make_response
from Backend.Services.view_test_results_service.service import get_test_results
app = Flask(__name__)


@app.route("/view-test_results", methods=['GET'])
def view_results():
    country = 'Ireland'
    get_test_results(country=country)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
