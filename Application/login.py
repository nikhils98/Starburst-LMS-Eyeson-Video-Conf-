from Application import  app
from Application import models
from flask import request, render_template, redirect, flash, session
import hashlib

@app.route('/login2', methods=['POST'])
def login2():
    # get form information
    formData = request.form

    # validation
    if formData['email'] == "":
        flash("The email field is required.")
        return redirect("/")
    if formData['password'] == "":
        flash("The password field is required.")
        return redirect("/")


    q = models.User.query.filter_by(email=formData['name'],password=hashlib.md5(formData['password'].encode()).hexdigest()).first()
    if q == None:
        print('Your email/password was incorrect.')
        flash("Your email/password was incorrect.")
        return redirect("/")

        # correct password
    session['isAdmin'] = 1 if q.userRole == models.UserRole.Admin else 0
    session['id'] = q.userId

    return redirect("/")


###REGISTER THE USER
@app.route('/register', methods=['GET', 'POST'])
def register():
    # form data is GET, so render template
    if request.method == 'GET':
        return render_template('register.html')

    # request method is POST, so do everything

    formData = request.form

    # form validation
    if formData['password'] == "" or formData['name'] == "" or formData['email'] == "":
        return "All text fields are required"
    if not 'isAdmin' in formData:
        isAdmin = 0
    else:
        isAdmin = 1

    q = models.User.query.filter_by(email=formData['email']).first()
    if q:
        return "User already exists with this email"

    user = models.User()
    user.name = formData['name']
    user.password = hashlib.md5(formData['password'].encode()).hexdigest()
    user.email = formData['email']
    if isAdmin:
        user.userRole = models.UserRole.Admin
    else:
        user.userRole = models.UserRole.User
    models.db.session.add(user)
    models.db.session.commit()

    print('The User was created')
    flash("The user was created")
    return redirect("/register/")