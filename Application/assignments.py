from Application import  app
from Application import models
from flask import request, render_template, redirect, flash, session
from datetime import datetime
import os
ASSIGNMENT_UPLOAD_FOLDER = 'assignments'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/assignment', methods=['POST'])
def createAssignment():
    formData = request.form
    assignmentName = formData['assignmentName']
    assignmentDesc = formData['assignmentDesc']
    assignmentDeadline = datetime.strptime(formData['assignmentDeadline'],'%Y-%m-%d')

    if assignmentDesc == '' or assignmentName == '':
        flash('assignment fields empty')
        return 'assignment fields empty'

    newAssignment = models.Assignment()
    newAssignment.assignmentDesc = assignmentDesc
    newAssignment.assignmentName = assignmentName
    newAssignment.assignmentDeadline = assignmentDeadline

    files = request.files.getlist("files")
    for file in files:
        path = os.path.join(PROJECT_DIR,ASSIGNMENT_UPLOAD_FOLDER, file.filename)
        file.save(path)
        newAssignmentFile = models.AssignmentFile()
        newAssignmentFile.filePath = path

        newAssignment.assignmentFiles.append(newAssignmentFile)

    models.db.session.add(newAssignment)
    models.db.session.commit()
    return 'uploaded!'