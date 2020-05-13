from Application import app, org
from Application import models
from flask import request, render_template, redirect, flash, session, send_file
from Application.decorators.authenticate import authenticate
from datetime import datetime
from werkzeug.utils import secure_filename
import os

ASSIGNMENT_UPLOAD_FOLDER = 'assignments'
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', str(org.orgId))


@app.route('/assignments/delete/<id>')
def deleteAssignment(id):
    if not id:
        flash("Assignment id is missing")
        return redirect('/home')
    else:
        ass = models.Assignment.query.filter_by(assignmentId=id).one()
        cid = str(ass.course.courseId)
        models.db.session.delete(ass)
        models.db.session.commit()
        flash("Successfully Deleted")

    return redirect('/assignments/' + cid)


# Get list of assignments By Course
@app.route('/assignments/<id>', methods=['GET'])
def getAssignmentsByCourse(id):
    assignments = models.Assignment.query.filter_by(courseId=id).all()
    enrollment = models.Enrollment.query.filter_by(courseId=id, userId=session['id']).first()

    isTeacher = enrollment.enrollmentRole == models.EnrollmentRole.Teacher

    filteredAssignments = []

    for ass in assignments:
        if ass.course.courseId == int(id):
            filteredAssignments.append(ass)

    return render_template('assignments.html', assignments=filteredAssignments, course_id=id, isTeacher=isTeacher)


@app.route('/assignments/detail/<id>', methods=['GET'])
def getAssignmentDetailById(id):
    assignment = models.Assignment.query.filter_by(assignmentId=id).first()

    if not assignment:
        flash('Assignment did not exist')
        return redirect('/home')

    isTeacher = models.Enrollment.query.filter_by(courseId=assignment.courseId, userId=session[
        'id']).first().enrollmentRole == models.EnrollmentRole.Teacher
    return render_template('assignment_detail.html', assignment=assignment, isTeacher=isTeacher)


@app.route('/asssignments/download/<id>', methods=['GET'])
def downloadAssignment(id):
    fileId = id
    if not fileId:
        flash('send file id')
        return 'send file id'
    q = models.AssignmentFile.query.filter_by(assignmentFileId=fileId).first()
    if not q:
        flash('No file found')
        return 'no file found'
    else:
        assFile = q
        return send_file(assFile.filePath, as_attachment=True)


@app.route('/createAssignment/<course_id>', methods=['GET', 'POST'])
@authenticate
def createAssignment(course_id):
    course = models.Course.query.filter_by(courseId=course_id).first()
    if not course:
        flash('No Course for this to create Assignment')
        return redirect('/home')

    assignments = models.Assignment.query.filter_by(courseId=course_id).all()
    filteredAssignments = []
    for ass in assignments:
        if ass.course.courseId == int(course_id):
            filteredAssignments.append(ass)

    formData = request.form
    assignmentName = formData['assignmentName']
    assignmentDesc = formData['assignmentDesc']
    totalMarks = formData['totalMarks']

    print(assignmentName, assignmentDesc, formData["assignmentDeadline"], totalMarks)
    if assignmentDesc == '' or assignmentName == '' or totalMarks == '':
        # flash('assignment fields empty')
        return render_template('assignments.html', course_id=course_id,
                               assignments=filteredAssignments,
                               err_msg='Fields cannot be left empty',
                               assignment_name=assignmentName,
                               assignment_desc=assignmentDesc,
                               total_marks=totalMarks,
                               show_modal=True)
    # We need to include time here as well. When u change it to that: DONE
    try:
        assignmentDeadline = datetime.strptime(formData['assignmentDeadline'], '%Y/%m/%d %H:%M')
    except ValueError:
        # flash('Please enter date time field')
        return render_template('assignments.html', course_id=course_id,
                               err_msg='Assignment Due Date must not be empty. ',
                               assignments=filteredAssignments,
                               assignment_name=assignmentName,
                               assignment_desc=assignmentDesc,
                               total_marks=totalMarks,
                               show_modal=True)

    newAssignment = models.Assignment()
    newAssignment.assignmentDesc = assignmentDesc
    newAssignment.assignmentName = assignmentName
    newAssignment.assignmentDeadline = assignmentDeadline
    newAssignment.uploadDateTime = datetime.today()
    newAssignment.totalMarks = float(totalMarks)
    newAssignment.courseId = course.courseId

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
            newAssignmentFile.fileName = file.filename
            models.db.session.add(newAssignmentFile)

    models.db.session.commit()
    flash("Assignment successfully created")
    return getAssignmentsByCourse(id=course_id)


@app.route('/updateAssignment/<id>', methods=['GET', 'POST'])
@authenticate
def updateAssignment(id):
    assignment = models.Assignment.query.filter_by(assignmentId=id).first()
    if not assignment:
        flash('No Assignment for this to update Assignment')
        return redirect('/home')
    # making a files directory to keep things tidy. Also easy to add in gitignore
    if request.method == 'GET':
        return render_template('update_assignment_page.html', assignment=assignment)
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
            return render_template('update_assignment_page.html', assignment=assignment)

        if assignmentDesc == '' or assignmentName == '' or totalMarks == '':
            flash('assignment fields empty')
            return render_template('update_assignment_page.html', assignment=assignment)

        assignment.assignmentDesc = assignmentDesc
        assignment.assignmentName = assignmentName
        assignment.assignmentDeadline = assignmentDeadline
        assignment.uploadDateTime = datetime.today()
        assignment.totalMarks = float(totalMarks)

        # to get the assignmentId. Unlike commit, flush kinda communicates the changes
        # to db but they're not persisted in disk. Commit ensures data is written to disk
        models.db.session.add(assignment)
        models.db.session.flush()

        files = request.files.getlist("files")

        # this is needed to create dir if it doesn't exist, otherwise file.save fails.
        assignmentDir = os.path.join(PROJECT_DIR, ASSIGNMENT_UPLOAD_FOLDER, str(assignment.assignmentId))

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
                newAssignmentFile.assignmentId = assignment.assignmentId
                newAssignmentFile.fileName = file.filename
                models.db.session.add(newAssignmentFile)

        models.db.session.commit()
        flash("Assignment successfully created")
        return getAssignmentsByCourse(id=assignment.courseId)
