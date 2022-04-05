from flask import Flask, make_response, jsonify
from flask_cors import CORS
from service import get_test_results

import logging

from utils import country_list


app = Flask(__name__)
CORS(app)


@app.route("/view-test-results/<string:country>", methods=["GET"])
def view_results(country: str):
    """
    Fetch test results
    :param country: Country whose test results are asked
    :return: json data
    """

    if country in country_list:
        return get_test_results(country=country)
    else:
        response = make_response(
                jsonify(
                    {"message": "Invalid country name {country}"}
                ),
                400,
            )
        response.headers["Content-Type"] = "application/json"
        return response



if __name__ == '__main__':
    app.run(debug=True, port=3000)

if __name__ != "__main__":
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("View test results service is now running!")
