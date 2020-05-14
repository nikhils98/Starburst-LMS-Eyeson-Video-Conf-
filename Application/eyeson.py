from Application import app
from Application import models
from Application.decorators.authenticate import authenticate
from flask import request, render_template, redirect, flash, session, jsonify
import requests
from markupsafe import escape
import hashlib


@app.route('/lectures/<courseId>', methods=['GET', 'POST'])
def lectures(courseId):
    cid = escape(courseId)

    if request.method == 'GET':
        lectures = models.Lecture.query.filter_by(courseId=cid).all()
        return render_template("lectures.html", lectures=lectures)

    formData = request.form
    #roomName = formData['roomName']
    roomName = None
    days = []
    for day in formData['days[1]']:
        days.append(day)

    for d in days:
        print(d)

    if not roomName:
        return redirect('lectures')

    userName = session['userName']
    url = "https://api.eyeson.team/rooms?user[name]=" + userName + "&name=" + roomName

    response = requests.post(url,
         headers={'Authorization': 'cAjgefMycsKmJc5qn553oWCUBSkPat35yXVu1pTnEf'}
     )

    print(response.json())
    # update = requests.post("https://api.eyeson.team/webhooks?"
    #                        "url=http://hec-lms.southeastasia.cloudapp.azure.com/recording_update&"
    #                        "types=recording_update",
    #                        headers={'Authorization': 'cAjgefMycsKmJc5qn553oWCUBSkPat35yXVu1pTnEf'})
    # print(update.status_code)

    return redirect('lectures/' + cid)


# @app.route('/recording_update', methods=['GET', 'POST'])
# def recording_update():
#     newClass = models.Class()
#     newClass.courseId = 1
#     newClass.className = "testing"
#     newClass.recordingLink = str(request.get_json())
#     models.db.session.add(newClass)
#     models.db.session.commit()
#     return jsonify(success=True)
