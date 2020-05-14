from datetime import datetime
from Application import app
from Application import models
from Application.decorators.authenticate import authenticate
from flask import request, render_template, redirect, flash, session, jsonify
import requests
from markupsafe import escape
import hashlib

AUTHORIZATION_KEY = 'cAjgefMycsKmJc5qn553oWCUBSkPat35yXVu1pTnEf'

@app.route('/lectures/<courseId>', methods=['GET', 'POST'])
@authenticate
def lectures(courseId):
    cid = escape(courseId)

    lectures = models.Lecture.query.filter_by(courseId=cid).all()
    if request.method == 'GET':
        return render_template("lectures.html", lectures=lectures, courseId=cid,
                               isTeacher=session['isTeacher'])

    formData = request.form
    name = formData['lectureName']
    agenda = formData['lectureAgenda']
    startDatetime = formData['startDatetime']

    if not name:
        name = 'Lecture'
    if not agenda:
        agenda = 'Not Provided'
    if not startDatetime:
        return render_template("lectures.html", lectures=lectures, courseId=cid,
                               isTeacher=session['isTeacher'], err_msg='Please select a time',
                               lecture_name=name, lecture_agenda=agenda, show_modal=True)

    userName = session['userName']
    url = "https://api.eyeson.team/rooms?user[name]=" + userName + "&name=" + name

    response = requests.post(url, headers={'Authorization': AUTHORIZATION_KEY})

    lecture = models.Lecture()
    lecture.courseId = cid
    lecture.lectureName = name
    lecture.lectureAgenda = agenda
    lecture.startDatetime = datetime.strptime(startDatetime, '%Y/%m/%d %H:%M')
    lecture.hostLink = response.json()['links']['gui']
    lecture.guestLink = response.json()['links']['guest_join']
    lecture.videoAccessKey = response.json()['access_key']
    lecture.videoRoomId = response.json()['room']['id']

    models.db.session.add(lecture)
    models.db.session.commit()

    flash("Lecture has been scheduled")
    return redirect('/lectures/' + cid)

@app.route('/deleteLecture/<courseId>/<id>')
@authenticate
def deleteLecture(courseId, id):
    cid = escape(courseId)
    lid = escape(id)

    lecture = models.Lecture.query.filter_by(lectureId=lid).first()

    if not lecture:
        flash("Lecture not found")
    else:
        res = requests.delete("https://api.eyeson.team/rooms/" + lecture.videoRoomId,
                              headers={'Authorization': AUTHORIZATION_KEY})
        print(res.status_code)
        models.db.session.delete(lecture)
        models.db.session.commit()

    return redirect('/lectures/' + cid)
