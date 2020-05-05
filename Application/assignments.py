from Application import app, org
from Application import models
from flask import request, render_template, redirect, flash, session, send_file
from Application.decorators.authenticate import authenticate
from datetime import datetime
from werkzeug.utils import secure_filename
import os

ASSIGNMENT_UPLOAD_FOLDER = 'assignments'
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', str(org.orgId))


@app.route('/downloadAssignment', methods=['GET'])
def downloadAssignment():
    fileId = request.args.get('id')
    if not fileId:
        flash('send file id')
        return 'send file id'
    q = models.AssignmentFile.query.filter_by(assignmintFileId=fileId).first()
    if not q:
        flash('No file found')
        return 'no file found'
    else:
        assFile = q
        return send_file(assFile.filePath, as_attachment=True)


@app.route('/createAssignment', methods=['GET', 'POST'])
@authenticate
def createAssignment():
    # making a files directory to keep things tidy. Also easy to add in gitignore

    if request.method == 'GET':
        return render_template('create_assignment_modal.html')
    else:
        formData = request.form
        assignmentName = formData['assignmentName']
        assignmentDesc = formData['assignmentDesc']
        totalMarks = formData['totalMarks']

        print(assignmentName, assignmentDesc, formData["assignmentDeadline"], totalMarks)
        # We need to include time here as well. When u change it to that: DONE
        try:
            assignmentDeadline = datetime.strptime(formData['assignmentDeadline'], '%Y/%m/%d %H:%M')
        except ValueError:
            flash('Please enter date time field')
            return render_template('create_assignment_modal.html')

        if assignmentDesc == '' or assignmentName == '' or totalMarks == '':
            flash('assignment fields empty')
            return render_template('create_assignment_modal.html')

        newAssignment = models.Assignment()
        newAssignment.assignmentDesc = assignmentDesc
        newAssignment.assignmentName = assignmentName
        newAssignment.assignmentDeadline = assignmentDeadline
        newAssignment.uploadDateTime = datetime.today()
        newAssignment.totalMarks = float(totalMarks)

        # to get the assignmentId. Unlike commit, flush kinda communicates the changes
        # to db but they're not persisted in disk. Commit ensures data is written to disk
        models.db.session.add(newAssignment)
        models.db.session.flush()

        files = request.files.getlist("files")

        # this is needed to create dir if it doesn't exist, otherwise file.save fails.
        assignmentDir = os.path.join(PROJECT_DIR, ASSIGNMENT_UPLOAD_FOLDER, str(newAssignment.assignmentId))

        for file in files:
            # for some reason when not uploading any file it was still reaching this code
            # with an empty file so I included this check for now
            if file:
                if not os.path.exists(assignmentDir):
                    os.makedirs(assignmentDir)
                path = os.path.join(assignmentDir, secure_filename(file.filename))
                file.save(path)
                newAssignmentFile = models.AssignmentFile()
                newAssignmentFile.filePath = path
                newAssignmentFile.assignmentId = newAssignment.assignmentId

                models.db.session.add(newAssignmentFile)

    models.db.session.commit()
    flash("Successfully created")
    return render_template('create_assignment_modal.html')
