#auth file deals with logging in and sign in/up features
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_bcrypt import generate_password_hash, check_password_hash    #we generate a password hash
from flask_login import login_user, logout_user, login_required     #we import the login fcts 
from .models import User    #we import the user and table
from . import db

auth = Blueprint('auth', __name__)      #we set up our auth blueprint

@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()    #we filter the user to see if it exists

    if not user or not check_password_hash(user.password, password):    #take the user supplied password, hash it, and compare it to the hashed password in database
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('auth.login'))    #if the user or password doesn't match we return the user to login page   
    else:
        login_user(user, remember=remember)     #we log the user in
        return redirect(url_for('main.profile'))    #if it exists we redirect to main profile

#we create and define our page(s)
@auth.route('/signup', methods=['GET'])     #setting the route to the page(s)
def signup():     #this is the function that will be called when the user visits the designated page(s)
    return render_template('signup.html')     #rendering the page(s)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
#if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()    # we filter the user to see if it exists

    if user:    #if a user is found, we want to redirect back to signup page so user can try again
        flash('Email already exists. Please choose another email.', 'error')
        return redirect(url_for('auth.signup'))     #if the user exists, we redirect to singup page
    else:
        #if the user does not exist we create a new user
        new_user = User(email=email, name=name, password=generate_password_hash(password).decode('utf-8'))    #we generate a instance of the user table
        db.session.add(new_user)    #we add the new user to the db
        db.session.commit()
        flash('Signup successful. You can now log in.', 'success')
        return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():     #we log the user out and redirect to homepage
    logout_user()   #this decorator checks if user is logged in or not before logingout
    return redirect(url_for('main.index'))
