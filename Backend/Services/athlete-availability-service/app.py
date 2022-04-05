import logging
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import logging

import services
import models
import forms
from settings import *
from auth import token_required, WADA, ATHLETE, ORCHESTRATOR

app = Flask(__name__)
CORS_ALLOW_ORIGIN = "*,*"
CORS_EXPOSE_HEADERS = "*,*"
CORS_ALLOW_HEADERS = "content-type,*"
CORS(app, origins=CORS_ALLOW_ORIGIN.split(","),
        allow_headers=CORS_ALLOW_HEADERS.split(","), 
        expose_headers=CORS_EXPOSE_HEADERS.split(","),   
        supports_credentials=True)


#for request format see readme
@app.route("/update-athlete-availability", methods=['OPTIONS','GET','POST'])
@token_required([ATHLETE])
def update_availability():
    if (request.method == "OPTIONS"):
        return build_preflight_response(), 200

    if request.method == 'POST':
        data = request.get_json()[0]
        availability_form = forms.convert_data_to_form(data)

        if availability_form.validate():
            
            try: 
                athlete_availability: models.AthleteAvailability = models.AthleteAvailability(availability_form)
            except Exception as e:
                return make_response(str(e), 400)

            if type(athlete_availability) is str:
                return(make_response(athlete_availability, 403))

            try: 
                resp = services.create_availability(athlete_availability)
                if resp:
                    return make_response(UPDATE_SUCCESS, 200)
            
            except Exception as e:
                return make_response(str(e), 403)
    else:
        return jsonify({
            'form': {
                'athlete_id': 'str',
                'date_time_utc': 'str',
                'location': 'str',
                'country': 'str'
                }
            })
       
        
@app.route("/view-athlete-availability/<string:athlete_id>", methods=['GET'])
@token_required([ORCHESTRATOR, WADA])
def view_availability(athlete_id: str):
    if request.method == 'GET':
        try:
            if athlete_id:
                resp = services.get_availability(athlete_id)
                return make_response(jsonify(resp), 200)
            else: 
                return make_response(NOT_ATHLETE_ID, 403)
        except Exception as e:
            return make_response(str(e), 404)

    else:
        return make_response(NOT_ATHLETE_ID, 403) 
        

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)


if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Create account service is now running!")