from flask import Flask, jsonify, request
from dynamo_handler import *
from flask import Response

app = Flask(__name__)


@app.route("/create-athlete-account", methods=['GET', 'POST'])
def create_athlete_account():
    if request.method == 'POST':
        
        data = request.get_json()
        
        adoAtheltedict = {
            'Ado': data['Ado'],
            'AthleteId': data['AthleteId']
        }
        
        # check if data exists in adoAthelte table
        # if not, return invalid data error        
        response = check_if_id_exists_in_table(**adoAtheltedict)
        
        if response.get('error'):
            return Response(response.get('error'), response.get('status_code'))
        
        #account exists in adoAthlete, now update users table
        
        # data validation needed
        
        user_profile_data = {
            'Organization': data['Ado'],
            'Id': data['AthleteId'],
            'FirstName': data['FirstName'],
            'LastName': data['LastName'],
            'Email': data['Email'],
            'Country': data['Country'],
            'PhoneNumber': data['PhoneNumber']
        }
        
        
        response = create_user_if_not_exists(**user_profile_data)
        
        return jsonify(response)
        
        return jsonify({'message': 'Successfully created athlete account'})
        # if it exists, create athelte account in users table 
        
        
        
        
        
    else:
        return jsonify({"error": "Method not allowed"})


@app.route("/create-ado-account", methods=['GET', 'POST'])
# pass the ado name and email to this account, passoword is created in the db 
def stuff2():
    return 'ok'


@app.route("/create-tester-account", methods=['GET', 'POST'])
def stuff():
    return 'ok'
# pass the tester name and email to this account, passoword is created


if __name__ == "__main__":
    app.run(port=5000, debug=True)