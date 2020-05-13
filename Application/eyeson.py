from Application import app
from Application import models
from Application.decorators.authenticate import authenticate
from flask import request, render_template, redirect, flash, session, jsonify
import requests
import hashlib


@app.route('/meetings', methods=['GET'])
def meetings():
    return render_template("meetings.html")


@app.route('/createMeeting')
def createMeeting():
    response = requests.post("https://api.eyeson.team/rooms?user[name]=nikhilsatiani",
                             headers={'Authorization': 'cAjgefMycsKmJc5qn553oWCUBSkPat35yXVu1pTnEf'})
    print(response.json())
    update = requests.post("https://api.eyeson.team/webhooks?"
                           "url=http://hec-lms.southeastasia.cloudapp.azure.com/recording_update&"
                           "types=recording_update",
                           headers={'Authorization': 'cAjgefMycsKmJc5qn553oWCUBSkPat35yXVu1pTnEf'})
    print(update.status_code)
    return render_template('meetings.html', room=response.json())


@app.route('/recording_update', methods=['GET', 'POST'])
def recording_update():
    print(request.get_json())
    return jsonify(success=True)
