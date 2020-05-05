from Application import app, org
from Application import models
from flask import request, render_template, redirect, flash, session, send_file
from Application.decorators.authenticate import authenticate
from datetime import datetime
from werkzeug.utils import secure_filename
import os

ASSIGNMENT_UPLOAD_FOLDER = 'assignments'
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', str(org.orgId))

