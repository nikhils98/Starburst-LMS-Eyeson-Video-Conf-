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
user.name = 'nikhil'
user.email = 'nikhil.satiani@gmail.com'
user.password = hashlib.md5('nikhil'.encode()).hexdigest()
user.userRole = models.UserRole.User
user.orgId = 1

models.db.session.add(user)

models.db.session.commit()


user = models.User()
user.name = 'sualeh'
user.email = 'sualeh.ali@gmail.com'
user.password = hashlib.md5('sualeh'.encode()).hexdigest()
user.userRole = models.UserRole.User
user.orgId = 1

models.db.session.add(user)

course1 = models.Course()
course1.courseName = 'SPM'
course1.courseDesc = 'Good course'
course1.courseSemester = 'Spring'
course1.courseYear = '2020'

course2 = models.Course()
course2.courseName = 'Pol Sci'
course2.courseDesc = 'Good course'
course2.courseSemester = 'Spring'
course2.courseYear = '2020'

models.db.session.add(course1)
models.db.session.add(course2)

e1 = models.Enrollment()
e1.userId = 1
e1.courseId = 1
e1.enrollmentRole = models.EnrollmentRole.Teacher

e2 = models.Enrollment()
e2.userId = 1
e2.courseId = 2
e2.enrollmentRole = models.EnrollmentRole.Student

e3 = models.Enrollment()
e3.userId = 2
e3.courseId = 1
e3.enrollmentRole = models.EnrollmentRole.Student

models.db.session.add(e1)
models.db.session.add(e2)
models.db.session.add(e3)

assign = models.Assignment()
assign.courseId = 1
assign.assignmentDeadline = datetime.datetime.today()
assign.assignmentDesc = "krle bhai"
assign.assignmentName = "testing"
assign.totalMarks = 10.5
assign.uploadDateTime = datetime.datetime.today()

models.db.session.add(assign)


assign = models.Assignment()
assign.courseId = 2
assign.assignmentDeadline = datetime.datetime.today()
assign.assignmentDesc = "Lamba sa Research Paper"
assign.assignmentName = "20000 Word Research Paper"
assign.totalMarks = 9000
assign.uploadDateTime = datetime.datetime.today()
models.db.session.add(assign)


sub = models.AssignmentSubmission()
sub.assignmentId = 1
sub.userId = 1
sub.submissionTime = datetime.datetime.today()
sub.comment = 'Im awesome, please give me full marks'


models.db.session.add(sub)

sub = models.AssignmentSubmission()
sub.assignmentId = 1
sub.userId = 2
sub.submissionTime = datetime.datetime.today()
sub.comment = 'Im awesome, please give me full marks'

models.db.session.add(sub)

models.db.session.commit()

from . import views, login, assignments, resources, assignment_submissions, eyeson
