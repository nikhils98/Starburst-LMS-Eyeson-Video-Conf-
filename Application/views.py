from Application import app
from flask import render_template, url_for

@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/')
def login():
    return render_template('index.html')