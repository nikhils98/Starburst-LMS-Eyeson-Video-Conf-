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
    newClass = models.Class()
    newClass.courseId = 1
    newClass.className = "testing"
    newClass.recordingLink = str(request.get_json())
    models.db.session.add(newClass)
    models.db.session.commit()
    return jsonify(success=True)

@app.route('/classes')
def classes():
    classes = models.Class.query.all()
    return render_template("classes.html", classes=classes)
