import hashlib
import os
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import session

# from flask_migrate import Migrate
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "starburst.db"))

print(database_file)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.secret_key = 'secret_key_yo'

db = SQLAlchemy(app)

from . import models

db.drop_all()
db.create_all()

# dummy data initialization
org = models.Organization()
org.orgName = 'IBA'

models.db.session.add(org)

user = models.User()
user.name = 'Nikhil Satiani'
user.email = 'nikhil.satiani@gmail.com'
user.password = hashlib.md5('nikhil'.encode()).hexdigest()
user.userRole = models.UserRole.User
user.orgId = 1

models.db.session.add(user)

user = models.User()
user.name = 'Sualeh Ali'
user.email = 'sualeh.ali@gmail.com'
user.password = hashlib.md5('sualeh'.encode()).hexdigest()
user.userRole = models.UserRole.User
user.orgId = 1

models.db.session.add(user)

course = models.Course()
course.courseName = 'SPM'
course.courseDesc = 'This is course description'
course.courseSemester = 'Spring'
course.courseYear = '2020'

models.db.session.add(course)

course = models.Course()
course.courseName = 'Intro to Political Science'
course.courseDesc = 'Description'
course.courseSemester = 'Spring'
course.courseYear = '2020'

models.db.session.add(course)

course = models.Course()
course.courseName = 'Distributed Systems'
course.courseDesc = 'Description'
course.courseSemester = 'Spring'
course.courseYear = '2020'

models.db.session.add(course)

course = models.Course()
course.courseName = 'Audit'
course.courseDesc = 'Description'
course.courseSemester = 'Spring'
course.courseYear = '2020'

models.db.session.add(course)

enroll = models.Enrollment()
enroll.userId = 1
enroll.courseId = 1
enroll.enrollmentRole = models.EnrollmentRole.Teacher

models.db.session.add(enroll)

enroll = models.Enrollment()
enroll.userId = 2
enroll.courseId = 1
enroll.enrollmentRole = models.EnrollmentRole.Student

models.db.session.add(enroll)

enroll = models.Enrollment()
enroll.userId = 2
enroll.courseId = 2
enroll.enrollmentRole = models.EnrollmentRole.Student

models.db.session.add(enroll)

enroll = models.Enrollment()
enroll.userId = 2
enroll.courseId = 3
enroll.enrollmentRole = models.EnrollmentRole.Student

models.db.session.add(enroll)

enroll = models.Enrollment()
enroll.userId = 2
enroll.courseId = 4
enroll.enrollmentRole = models.EnrollmentRole.Student

models.db.session.add(enroll)

assign = models.Assignment()
assign.courseId = 1
assign.assignmentDeadline = datetime.datetime.today() + datetime.timedelta(days=5)
assign.assignmentDesc = "This is assignment description"
assign.assignmentName = "Iron Triangle"
assign.totalMarks = 10
assign.uploadDateTime = datetime.datetime.today()

models.db.session.add(assign)

assign = models.Assignment()
assign.courseId = 2
assign.assignmentDeadline = datetime.datetime.today() + datetime.timedelta(days=10)
assign.assignmentDesc = "Research Paper"
assign.assignmentName = "2000 Word Research Paper"
assign.totalMarks = 20
assign.uploadDateTime = datetime.datetime.today()

models.db.session.add(assign)

sub = models.AssignmentSubmission()
sub.assignmentId = 1
sub.userId = 2
sub.submissionTime = datetime.datetime.today()
sub.comment = 'Im awesome, please give me full marks'

models.db.session.add(sub)

sub = models.AssignmentSubmission()
sub.assignmentId = 2
sub.userId = 2
sub.submissionTime = datetime.datetime.today()
sub.comment = 'Im awesome, please give me full marks'

models.db.session.add(sub)

models.db.session.commit()

from . import views, login, assignments, resources, assignment_submissions, lectures, recordings
