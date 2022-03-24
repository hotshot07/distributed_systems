from flask import Flask, request, make_response, jsonify

import services
import models
import forms
from settings import *

app = Flask(__name__)

#for request format see readme
@app.route("/update-athlete-availability", methods=['GET','POST'])
def update_availability():
    if request.method == 'POST':
        data = request.get_json()[0]
        availability_form = forms.convert_data_to_form(data)

        if availability_form.validate():
            
            try: 
                athlete_availability: AthleteAvailability = models.AthleteAvailability(availability_form)
            except Exception as e:
                return make_response(str(e), 400)

            if type(athlete_availability) is str:
                return(make_response(athlete_availability, 403))

            try: 
                resp = services.update_availability(athlete_availability)
                if resp:
                    return make_response(UPDATE_SUCCESS, 200)
            
            except Exception as e:
                return make_response(COULD_NOT_CREATE_ITEM, 403)
    else:
        return jsonify({
            'form': {
                'athlete_id': 'str',
                'date_time_utc': 'str',
                'location': 'str',
                'country': 'str'
                }
            })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)