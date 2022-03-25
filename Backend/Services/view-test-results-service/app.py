from flask import Flask
from service import get_test_results
from utils import country_list

app = Flask(__name__)


@app.route("/view-test-results/<string:country>", methods=["GET"])
def view_results(country: str):
    """
    Fetch test results
    :param country: Country whose test results are asked
    :return: json data
    """
    if country.capitalize() in country_list:
        return get_test_results(country=country.capitalize())
    else:
        return f"Invalid country name {country}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
