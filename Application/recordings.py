from datetime import datetime
from Application import app
from Application import models
from Application.decorators.authenticate import authenticate
from flask import request, render_template, redirect, flash, session, jsonify
import requests
from markupsafe import escape
import hashlib

AUTHORIZATION_KEY = 'cAjgefMycsKmJc5qn553oWCUBSkPat35yXVu1pTnEf'


@app.route('/recordings/<lectureId>')
@authenticate
def recordings(lectureId):
    lid = escape(lectureId)

    recs = models.Recording.query \
        .filter_by(lectureId=lid) \
        .filter(models.Recording.link is not None) \
        .all()

    links = []
    for r in recs:
        links.append(r.link)

    return jsonify(links=links)


@app.route('/startRecording/<lectureId>')
@authenticate
def startRecording(lectureId):
    lid = escape(lectureId)

    lecture = models.Lecture.query.filter_by(lectureId=lid).first()

    if not lecture:
        print(lid)
        return jsonify(success=False)

    res = requests.post("https://api.eyeson.team/rooms/" + lecture.videoAccessKey + "/recording",
                        headers={'Authorization': AUTHORIZATION_KEY})
    if res.status_code == 201:
        res = requests.get("https://api.eyeson.team/rooms/" + lecture.videoAccessKey,
                           headers={'Authorization': AUTHORIZATION_KEY})

        recording = models.Recording()
        recording.lectureId = lid
        recording.identifier = res.json()['recording']['id']
        print(recording.identifier)

        models.db.session.add(recording)

        lecture.isRecordingActive = True

        models.db.session.commit()
    else:
        return jsonify(success=False)

    return jsonify(success=True, recordingId=recording.recordingId)


@app.route('/stopRecording/<lectureId>')
@authenticate
def stopRecording(lectureId):
    lid = escape(lectureId)

    lecture = models.Lecture.query.filter_by(lectureId=lid).first()

    if not lecture:
        return jsonify(success=False)

    res = requests.delete("https://api.eyeson.team/rooms/" + lecture.videoAccessKey + "/recording",
                          headers={'Authorization': AUTHORIZATION_KEY})

    if res.status_code == 200:
        recording = models.Recording.query \
            .filter_by(lectureId=lid) \
            .filter_by(link=None) \
            .first()
        print(recording.recordingId)
        res = requests.get("https://api.eyeson.team/recordings/" + recording.identifier,
                           headers={'Authorization': AUTHORIZATION_KEY})

        recording.link = res.json()['links']['download']

        lecture.isRecordingActive = False

        models.db.session.commit()
    else:
        return jsonify(success=False)

    return jsonify(success=True)
