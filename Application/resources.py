from Application import app, org
from Application import models
from flask import request, render_template, redirect, flash, session, send_file
from datetime import datetime
from werkzeug.utils import secure_filename
import os

RESOURCE_UPLOAD_FOLDER = 'resources'
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', str(org.orgId))

@app.route('/downloadResource',methods=['GET'])
def downloadResource():
    fileId = request.args.get('id')
    if not fileId:
        flash('send file id')
        return 'send file id'
    q = models.Resource.query.filter_by(resourceId=fileId).first()
    if not q:
        flash('No file found')
        return 'no file found'
    else:
        resource = q
        return send_file(resource.filePath,as_attachment=True)


@app.route('/createResource', methods=['GET', 'POST'])
def createResource():
    # making a files directory to keep things tidy. Also easy to add in gitignore
    if request.method == 'GET':
        return render_template('create_resource_modal.html')
    else:
        formData = request.form
        resourceName = formData['resourceName']


        if resourceName == '':
            flash('resource fields empty')
            return render_template('create_resource_modal.html')

        newResource = models.Resource()
        newResource.resourceName = resourceName

        if "file" not in request.files:
            flash('Please upload files')
            return render_template('create_resource_modal.html')

        file = request.files['file']
        # this is needed to create dir if it doesn't exist, otherwise file.save fails.
        assignmentDir = os.path.join(PROJECT_DIR, RESOURCE_UPLOAD_FOLDER)
        if not os.path.exists(assignmentDir):
            os.makedirs(assignmentDir)

        if file:
            path = os.path.join(assignmentDir, secure_filename(file.filename))
            file.save(path)
            newResource.filePath = path

            models.db.session.add(newResource)
            models.db.session.commit()
            return render_template('create_resource_modal.html')
        else:
            flash('couldnt upload :(')
            return render_template('create_resource_modal.html')