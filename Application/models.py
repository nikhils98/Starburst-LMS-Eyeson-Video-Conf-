import enum
from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
import datetime


db.create_all()
db.session.commit()


# TODO: Add Backrefs

class UserRole(enum.Enum):
    User = 1
    Admin = 2
class EnrollmentRole(enum.Enum):
    Teacher = 1
    Student = 2


class User(db.Model):

    # TODO: Add Support for organizations later

    __tablename__ = "users"
    # __table_args__ = {"schema": "starburst"}

    userId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(100),
        index=True,
        nullable=False,
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(255)
    )
    userRole = db.Column(Enum(UserRole))
    orgId = db.Column(db.Integer, db.ForeignKey('organizations.orgId'))
    organization = relationship("Organization")

class Organization(db.Model):
    __tablename__ = "organizations"
    # __table_args__ = {"schema": "starburst"}

    orgId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    orgName = db.String(120)

class Course(db.Model):
    __tablename__ = "courses"
    # __table_args__ = {"schema": "starburst"}

    courseId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    courseName = db.Column(
        db.String(120),
        index=True,
        nullable=False
    )
    courseDesc = db.Column(
        db.String(255),
        nullable=False
    )
    courseSemester = db.Column(
        db.String(50)
    )
    courseYear = db.Column(
        db.String(12),
    )

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    # __table_args__ = {"schema": "starburst"}

    enrollmentId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    courseId = db.Column(db.Integer, db.ForeignKey('courses.courseId'))
    course = relationship("Course", backref="enrollments")
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    user = relationship("User", backref="enrollments")

    enrollmentRole = db.Column(Enum(EnrollmentRole))

class Class(db.Model):
    __tablename__ = "classes"
    # __table_args__ = {"schema": "starburst"}

    classId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    className = db.Column(
        db.String(250),
        nullable=False
    )
    recordingLink = db.Column(
        db.String(400)
    )
    classLink = db.Column(
        db.String(400)
    )
    courseId = db.Column(db.Integer, db.ForeignKey('courses.courseId'))
    course = relationship("Course")

class Resource(db.Model):
    __tablename__ = "resources"
    # __table_args__ = {"schema": "starburst"}

    resourceId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    resourceName = db.Column(
        db.String(250),
        nullable=False
    )
    filePath = db.Column(
        db.String(250)
    )
    courseId = db.Column(db.Integer, db.ForeignKey('courses.courseId'))
    course = relationship("Course")


class Assignment(db.Model):
    __tablename__ = "assignments"
    # __table_args__ = {"schema": "starburst"}

    assignmentId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    assignmentName = db.Column(
        db.String(120),
        nullable=False
    )
    assignmentDesc = db.Column(
        db.String(255),
        nullable=False
    )
    assignmentDeadline = db.Column(
        db.DateTime
    )
    courseId = db.Column(db.Integer, db.ForeignKey('courses.courseId'))
    courses = relationship("Course")

class AssignmentFile(db.Model):
    __tablename__ = "assignment_files"
    # __table_args__ = {"schema": "starburst"}

    assignmentFileId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    filePath = db.Column(
        db.String(250),
        nullable=False
    )
    assignmentId = db.Column(db.Integer, db.ForeignKey('assignments.assignmentId'))
    assignments = relationship("Assignment",backref='assignmentFiles')

class AssignmentSubmission(db.Model):
    __tablename__ = "assignment_submissions"
    # __table_args__ = {"schema": "starburst"}

    assignmentSubmissionId = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    submissionTime = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    assignmentId = db.Column(db.Integer, db.ForeignKey('assignments.assignmentId'))
    assignment = relationship("Assignment")
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    user = relationship("User")

    gradeReceived = db.Column(
        db.String(10)
    )


