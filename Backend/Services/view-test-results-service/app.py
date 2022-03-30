from flask import Flask
from service import get_test_results
import logging

from utils import country_list

app = Flask(__name__)


@app.route("/view-test-results/<string:country>", methods=["GET"])
def view_results(country: str):
    """
    Fetch test results
    :param country: Country whose test results are asked
    :return: json data
    """

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
