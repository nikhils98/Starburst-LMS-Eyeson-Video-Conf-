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

from . import views, login, assignments, resources