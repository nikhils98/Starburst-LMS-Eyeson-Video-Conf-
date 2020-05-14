from sqlalchemy.orm import load_only

from Application import app
from Application import models
from flask import request, render_template, redirect, flash, session, url_for
from markupsafe import escape

from Application.decorators.authenticate import authenticate


@app.route('/home')
@authenticate
def index():
    name = request.args.get('name')
    #if request.args.get('name'):
    #    name = request.args.get('name')

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

    return render_template('home.html', courses=courses, name=name)

@app.route('/coursesite/<id>')
@authenticate
def coursesite(id):
    userId = session['id']
    courseId = escape(id)

    enrollment = models.Enrollment.query.filter_by(courseId=courseId, userId=userId).first()
    isTeacher = enrollment.enrollmentRole == models.EnrollmentRole.Teacher

    session['isTeacher'] = isTeacher

    return render_template('course_page.html', id=courseId, isTeacher=isTeacher)