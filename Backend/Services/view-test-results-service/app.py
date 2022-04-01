from flask import Flask
from service import get_test_results
import logging
from flask_caching import Cache
from utils import country_list

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route("/view-test-results/<string:country>", methods=["GET"])
@cache.cached(timeout=50)
def view_results(country: str):
    """
    Fetch test results
    :param country: Country whose test results are asked
    :return: json data
    """

    if country in country_list:
        return get_test_results(country=country)
    else:
        return f"Invalid country name {country}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

if __name__ != "__main__":
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("View test results service is now running!")
