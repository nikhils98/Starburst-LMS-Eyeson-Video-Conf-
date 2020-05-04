from sqlalchemy.orm import joinedload

from Application import app
from Application import models
from flask import request, render_template, redirect, flash, session, url_for

@app.route('/home')
def index():
    user_id = session['id']
    courses = models.db.session.query(models.Enrollment).filter(models.Enrollment.userId == user_id)\
        .options(joinedload('course')).all()

    print(courses)
    #courses = models.Enrollment.query.filter_by(user_id=user_id).select_from().all()

    return render_template('home.html')
