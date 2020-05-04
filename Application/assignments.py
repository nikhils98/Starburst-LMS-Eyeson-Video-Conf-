from Application import app
from Application import models
from flask import request, render_template, redirect, flash, session
from datetime import datetime
from werkzeug.utils import secure_filename
import os

ASSIGNMENT_UPLOAD_FOLDER = 'assignments'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/createAssignment', methods=['GET', 'POST'])
def createAssignment():
    if request.method == 'GET':
        return render_template('create_assignment_modal.html')
    else:
        formData = request.form
        assignmentName = formData['assignmentName']
        assignmentDesc = formData['assignmentDesc']

        assignmentDeadline = datetime.strptime(formData['assignmentDeadline'], '%Y-%m-%d')

        print(assignmentName, assignmentDesc, assignmentDeadline)

        if assignmentDesc == '' or assignmentName == '':
            flash('assignment fields empty')
            return 'assignment fields empty'

        newAssignment = models.Assignment()
        newAssignment.assignmentDesc = assignmentDesc
        newAssignment.assignmentName = assignmentName
        newAssignment.assignmentDeadline = assignmentDeadline

        files = request.files.getlist("files")
        assignmentDir = os.path.join(PROJECT_DIR, ASSIGNMENT_UPLOAD_FOLDER)
        if not os.path.exists(assignmentDir):
            os.makedirs(assignmentDir)
        for file in files:
            if file:
                path = os.path.join(assignmentDir, secure_filename(file.filename))
                file.save(path)
                newAssignmentFile = models.AssignmentFile()
                newAssignmentFile.filePath = path

                newAssignment.assignmentFiles.append(newAssignmentFile)

        models.db.session.add(newAssignment)
        models.db.session.commit()
        return 'uploaded!'
