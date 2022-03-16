from flask import Flask, request, make_response

import services

app = Flask(__name__)

#for request format see readme
@app.route("/update-athlete-availability", methods=['POST'])
def update_availability():
    if request.method == 'POST':
        data = request.get_json()
        country = data[0]['country']
        athlete_id = data[0]['athlete_id']
        availability = data[0]['availability']
        resp = services.update_availability(
            country, 
            athlete_id,
            availability
            )
        if resp:
            return resp
        else:
            return make_response('Updates could not be completed, item may not exist', 500)
    else:
        return make_response('Method not recognised, use POST', 405 )


@app.route("/initialise-athlete-availability", methods=['POST'])
def initialise_availability():
    if request.method == 'POST':
        data = request.get_json()
        country = data[0]['country']
        athlete_id = data[0]['athlete_id']
        resp = services.initialise_availability(
            country,
            athlete_id
        )
        if resp:
            return resp
        else:
            return make_response('Initialisation could not be completed, item may already exist', 500) 
    else:
        return make_response('Method Not Recognised, use POST', 405 )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='4446')