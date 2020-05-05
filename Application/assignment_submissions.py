from Application import app, org
from Application import models
from flask import request, render_template, redirect, flash, session, send_file
from Application.decorators.authenticate import authenticate
from datetime import datetime
from werkzeug.utils import secure_filename
import os

ASSIGNMENT_UPLOAD_FOLDER = 'assignments'
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', str(org.orgId))

@app.route('/assignmentSubmission')
@authenticate
def assignmentSubmission():
    return render_template('')

@app.route('/downloadSubmission')
@authenticate
def downloadSubmission():
    # logic for downloading

    # after successful download
    return redirect('assignmentSubmission')

@app.route('/submitAssignment', methods=["GET", "POST"])
@authenticate
def submit_assignment():
    if request.method == "GET":
        return render_template('submit_assignment_modal.html')
    # logic for submission
    formData = request.form

    submission = models.AssignmentSubmission()


    # after successful submission
    flash("Assignment Submitted")
    return redirect('assignmentSubmission')
