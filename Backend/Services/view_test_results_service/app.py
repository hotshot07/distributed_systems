from flask import Flask
from Backend.Services.view_test_results_service.service import get_test_results
app = Flask(__name__)


@app.route("/view-test-results/<string:country>", methods=['GET'])
def view_results(country: str):
    """
    Fetch test results
    :param country: Country whose test results are asked
    :return: json data
    """
    return get_test_results(country=country)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
