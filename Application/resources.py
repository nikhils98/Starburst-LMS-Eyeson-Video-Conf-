from Application import app, org
from Application import models
from flask import request, render_template, redirect, flash, session, send_file
from datetime import datetime
from werkzeug.utils import secure_filename
import os

RESOURCE_UPLOAD_FOLDER = 'resources'
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', str(org.orgId))


@app.route('/downloadResource', methods=['GET'])
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
        return send_file(resource.filePath, as_attachment=True)


# Get list of resources By Course
@app.route('/resources/<id>', methods=['GET'])
def getResourcesByCourse(id):
    resources = models.Resource.query.filter_by(courseId=id).all()

    return render_template('resources.html', resources=resources, course_id=id)


@app.route('/createResource/<courseId>', methods=['POST'])
def createResource(courseId):
    formData = request.form
    resourceName = formData['resourceName']

    if resourceName == '':
        flash('resource fields empty')
        return render_template('resources.html', isModalOpen=True)

    newResource = models.Resource()
    newResource.resourceName = resourceName
    newResource.courseId = courseId

    file = request.files['file']
    # this is needed to create dir if it doesn't exist, otherwise file.save fails.
    resourceDir = os.path.join(PROJECT_DIR, RESOURCE_UPLOAD_FOLDER)
    if not os.path.exists(resourceDir):
        os.makedirs(resourceDir)

    if file:
        path = os.path.join(resourceDir, secure_filename(file.filename))
        file.save(path)
        newResource.filePath = path

        models.db.session.add(newResource)
        models.db.session.commit()
        flash("Resource uploaded")
        return render_template('resources.html')
    else:
        flash('Please upload a file')
        return render_template('resources.html', isModalOpen=True, resourceName=resourceName)
