from sqlalchemy import text

from Application import app, org
from Application import models
from flask import request, render_template, redirect, flash, session, send_file
from Application.decorators.authenticate import authenticate
from datetime import datetime
from werkzeug.utils import secure_filename
from markupsafe import escape
import os

ASSIGNMENT_SUBMISSION_FOLDER = 'assignments/{}/submissions'
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', str(org.orgId))

@app.route('/assignmentSubmission/<id>')
@authenticate
def assignmentSubmission(id):
    assignmentId = escape(id)

    # this doesn't give the desired out but leaving here for reference if
    # needed to execute raw sql again
    # sql = text('select enrollmentRole from enrollments e '
    #           'inner join courses c on e.courseId = c.courseId '
    #           'inner join assignments a on a.courseId = c.courseId '
    #           'where a.assignmentId = :id')
    # enrollmentType = models.db.engine.execute(sql, id=3).fetchall()
    # print(enrollmentType)

    # to get the enrollmentRole. This is very inefficient i think
    # but gets the job done for now
    result = models.Assignment.query.filter_by(assignmentId=assignmentId).first()
    enrollments = result.course.enrollments
    enrollmentRole = [e for e in enrollments if e.userId == session['id']][0].enrollmentRole
    print(enrollmentRole)

    submissions = []

    if enrollmentRole == models.EnrollmentRole.Teacher:
        submissions = models.db.session.query(models.AssignmentSubmission)\
            .filter(models.AssignmentSubmission.assignmentId == assignmentId)\
            .all()
    else:
        submissions = models.db.session.query(models.AssignmentSubmission) \
            .filter(models.AssignmentSubmission.assignmentId == assignmentId) \
            .filter(models.AssignmentSubmission.userId == session['id']) \
            .all()

    print(submissions)
    return render_template('assignment_submission.html', submissions=submissions,
                           enrollmentRole=enrollmentRole)

@app.route('/downloadSubmission/<id>')
@authenticate
def downloadSubmission(id):
    submissionFileId = escape(id)

    submissionFile = models.SubmissionFile.query.filter_by(submissionFileId=submissionFileId).first()
    if not submissionFile:
        flash('No file found')
    else:
        return send_file(submissionFile.filePath, as_attachment=True)
    return redirect('assignmentSubmission')

@app.route('/submitAssignment/<id>', methods=["GET", "POST"])
@authenticate
def submitAssignment(id):
    if request.method == "GET":
        return render_template('submit_assignment_modal.html')
    # logic for submission
    formData = request.form

    submission = models.AssignmentSubmission()
    submission.assignmentId = escape(id)
    submission.userId = session["id"]
    # Technically not needed since default in db is currentime
    submission.submissionTime = datetime.today()
    submission.comment = formData["comment"]

    models.db.session.add(submission)
    models.db.session.flush()

    files = request.files.getlist("files")

    # this is needed to create dir if it doesn't exist, otherwise file.save fails.
    submissionDir = os.path.join(PROJECT_DIR, ASSIGNMENT_SUBMISSION_FOLDER.format(str(submission.assignmentId)),
                                 str(submission.assignmentSubmissionId))

    for file in files:
        if file:
            if not os.path.exists(submissionDir):
                os.makedirs(submissionDir)
            path = os.path.join(submissionDir, secure_filename(file.filename))
            file.save(path)
            submissionFile = models.SubmissionFile()
            submissionFile.filePath = path
            submissionFile.submissionId = submission.assignmentSubmissionId

            models.db.session.add(submissionFile)

    models.db.session.commit()

    # after successful submission
    flash("Assignment Submitted")
    return redirect('submitAssignment')


@app.route('/gradeAssignmentSubmission/<id>', methods=['GET', 'POST'])
def gradeAssignmentSubmission(id):
    result = models.AssignmentSubmission.query.filter_by(assignmentSubmissionId=id).first()
    if not result:
        flash('Assignment Submission does not exist')
        return redirect('submitAssignment')

    formData = request.form
    if 'assignmentGrade' not in formData:
        flash('Please send grade')
        return redirect('submitAssignment')

    grade = formData['assignmentGrade']


    result.assignmentGrade = grade
    models.db.session.add(result)
    models.db.session.commit()

    flash('Graded Assignment')
    return redirect('submitAssignment')



