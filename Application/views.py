from sqlalchemy.orm import load_only

from Application import app
from Application import models
from flask import request, render_template, redirect, flash, session, url_for

from Application.decorators.authenticate import authenticate


@app.route('/home')
@authenticate
def index():
    user_id = session['id']
    enrollments = models.db.session.query(models.Enrollment)\
        .filter(models.Enrollment.userId == user_id).all()

    courses = []
    for e in enrollments:
        courses.append(e.course)

    #courses = models.Enrollment.query.filter_by(user_id=user_id).select_from().all()

    return render_template('home.html', courses=courses)
