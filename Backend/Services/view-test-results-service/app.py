from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from service import get_test_results
from auth import token_required, WADA, ORCHESTRATOR, ADMIN

import logging
from flask_caching import Cache
from utils import country_list
from countries import country_dict


app = Flask(__name__)
cache = Cache(
    app,
    config={
        "CACHE_TYPE": "SimpleCache",
    },
)
CORS(app)


@app.route("/view-test-results/<string:country>", methods=["GET"])
@token_required([WADA, ORCHESTRATOR, ADMIN])
@cache.cached(timeout=50)
def view_results(country: str):
    """
    Fetch test results
    :param country: Country whose test results are asked
    :return: json data
    """
    print(request.__dict__)
    def validate_country(country):
        l_country = country.split()
        if len(l_country) > 0:
            for idx, word in enumerate(l_country):
                if word.lower() in ['of', 'the', 'former', 'part']:
                    l_country[idx] = word.lower()
                else:
                    l_country[idx] = word.capitalize()
                f_country = ' '.join(l_country)
            country = f_country
        return country

    country = validate_country(country)

    # country_id = country_dict[country]
    
    if country in country_list:
        country_id = str(country_dict[country])
        return get_test_results(country=country_id)
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
