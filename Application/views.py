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

    # enrollments = models.Enrollment.query\
    #     .filter(models.Enrollment.course.in_(courses))\
    #     .filter(models.Enrollment.enrollmentRole == models.EnrollmentRole.Teacher)\
    #     .all()
    #
    # instructors = []
    # for e in enrollments:
    #     instructors.append(e.user)

    #courses = models.Enrollment.query.filter_by(user_id=user_id).select_from().all()

    return render_template('home.html', courses=courses)

@app.route('/assignment')
@authenticate
def assignmentPage():
    return render_template('assignments.html')

@app.route('/coursesite/<id>')
@authenticate
def coursesite(id):
    user_id = session['id']
    # i changed the parameter type because this allows mandatory id passing
    return render_template('course_page.html', id=id)