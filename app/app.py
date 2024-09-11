"""
Flask App Routing file.
Email logic in core_functions.py
"""

from flask import Flask, request
from flask_cors import CORS
import json
from core_functions import csv_to_map, privacy_api

app = Flask(__name__)
cors = CORS(app, resources={r"/privacyAPI/*": {"origins": "http://localhost:3000"}})

# privacyAPI - initiates CCPA data delete requests
@app.route('/privacyAPI/v1/', methods=["POST"])
def execute_privacy_api():
    '''
    Runs the privacyAPI for live data brokers

    Cookie check: The cookie "live-test: true" is required to run this function
    '''
    usrjson = request.get_json()
    services = {}
    service_csv = 'services_list_06May2021.csv'
    if app.debug:
        service_csv = 'test_services.csv'
    all_services, top_choice, people_search = csv_to_map(service_csv)
    print("usrjson['usrchoice'] = ", usrjson['usrchoice'])
    if usrjson['usrchoice'] == 'all_services':
        services = all_services
    elif usrjson['usrchoice'] == 'top_choice':
        services = top_choice
    else:
        services = people_search
    return json.dumps({
        "return": privacy_api(usrjson, services)
    }), 200

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
