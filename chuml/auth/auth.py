# auth.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint, flash
from flask_login import login_user, logout_user, login_required, \
						current_user, UserMixin, AnonymousUserMixin

import hashlib
from chuml.utils import crypto

from chuml.utils import db
from chuml.utils.db import Column, Integer, String, Boolean, ForeignKey
from chuml.models import Anonymous, User

auth = Blueprint('auth', __name__, template_folder='templates',
				url_prefix="/auth")

hash = lambda str: hashlib.sha256(str.encode("utf-8")).hexdigest()

#temporary main page
@auth.route('/')
def index():
	return render_template('index.html')

@auth.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name)

@auth.route('/login')
def login():
	return render_template('login.html', next=request.args.get("next",default=""))

@auth.route('/login', methods=['POST'])
def login_post():
	name = request.form.get('username')
	pasw = request.form.get('password')
	remember = True # if request.form.get('remember') else False

	user = db.query(User).filter_by(name=name).one_or_none()

	if not user or user.pasw != hash(pasw + user.salt): 
		flash('Please check your login details and try again.')
		return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

	login_user(user, remember=remember)

	next = request.form.get('next')
	if next:
		return redirect(next)
	else:
		return redirect(url_for('auth.profile'))

@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
	name = request.form.get('username')
	pasw = request.form.get('password')

	user = db.query(User).filter_by(name=name).one_or_none()

	if user or name in ["guest", "admin"]:
		flash("Username " + name + " already registred.")
		return redirect(url_for('auth.signup'))


	user = add_user(name, pasw)

	login_user(user)

	flash(name + " successfully signed up.")

	if "redirect" in request.args:
		return redirect(request.args.get("redirect"))
	else:
		return redirect(url_for('auth.profile'))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.index'))

def add_user(name, pasw):
	salt = crypto.get_random_iid()
	pasw = hash(pasw + salt)

	user = User(
		name=name,
		pasw=pasw,
		salt=salt
		)
	db.add(user)
	db.commit()

	return user
