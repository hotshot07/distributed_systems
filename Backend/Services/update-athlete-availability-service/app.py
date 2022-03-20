from flask import Flask, request, make_response

import services
import util
from settings import *

app = Flask(__name__)

#for request format see readme
@app.route("/update-athlete-availability", methods=['POST'])
def update_availability():
    if request.method == 'POST':
        data = request.get_json()
        availability = util.create_and_validate(data)
        if availability == 0:
            return make_response(INVALID_REQUEST_BODY, 400)
        if type(availability) == str:
            return make_response(availability, 400)
            
        resp = services.update_availability(availability)
        if resp:
            return resp
        else:
            return make_response(ITEM_DOES_NOT_EXIST, 403)
    else:
        return make_response(METHOD_NOT_FOUND, 405 )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4446')