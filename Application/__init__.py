import hashlib
import os

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
e1.enrollmentRole = models.EnrollmentRole.Student

e2 = models.Enrollment()
e2.userId = 1
e2.courseId = 2
e2.enrollmentRole = models.EnrollmentRole.Student

models.db.session.add(e1)
models.db.session.add(e2)

models.db.session.commit()

from . import views, login, assignments, resources
