from flask import Flask, request, make_response

import services
from settings import *

app = Flask(__name__)

#for request format see readme
@app.route("/update-athlete-availability", methods=['POST'])
def update_availability():
    if request.method == 'POST':
        data = request.get_json()
        athlete_id = data[0]['athlete_id']
        date_time_utc = data[0]['datetimeUTC']
        location = data[0]['location']
        country = data[0]['location_country']
        
        resp = services.update_availability(
            athlete_id,
            date_time_utc,
            location,
            country
            )
        if resp:
            return resp
        else:
            return make_response(ITEM_DOES_NOT_EXIST, 403)
    else:
        return make_response(METHOD_NOT_FOUND, 405 )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4446')