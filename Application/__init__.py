from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# from flask_migrate import Migrate
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "starburst.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

from . import views
