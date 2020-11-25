# auth.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint, flash
from flask_login import login_user, logout_user, login_required, \
						current_user, UserMixin, AnonymousUserMixin

import hashlib
from chuml.utils import crypto

from chuml.utils import db

auth = Blueprint('auth', __name__, template_folder='templates',
				url_prefix="/auth")

hash = lambda str: hashlib.sha256(str.encode("utf-8")).hexdigest()
users_table = db.table("users")

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
	return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
	username = request.form.get('username')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User(username)

	if not username in db.table("users") or \
	   user.pasw != hash(password + user.salt): 
		flash('Please check your login details and try again.')
		return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

	login_user(user, remember=remember)
	if "redirect" in request.args:
		return redirect(request.args.get("redirect"))
	else:
		return redirect(url_for('auth.profile'))

@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
	username = request.form.get('username')
	password = request.form.get('password')

	if username in db.table("users") + ["guest", "admin"]:
		flash("Username " + username + " already registred.")
		return redirect(url_for('auth.signup'))

	salt = crypto.get_random_iid()
	pasw = hash(password + salt)
	users_table[username] = {
		"pasw": pasw,
		"salt": salt
	}
	users_table.commit()

	user = User(username)
	login_user(user)

	flash(username + " successfully signed up.")

	if "redirect" in request.args:
		return redirect(request.args.get("redirect"))
	else:
		return redirect(url_for('auth.profile'))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	print(current_user.name)
	return redirect(url_for('auth.index'))

class User(UserMixin):
	def __init__(self, name):
		self.name = name
		try:
			data = db.table("users")[name]
		except KeyError:
			data = {}

		self.pasw = data.get("pasw")
		self.salt = data.get("salt")

	def get_id(self):
		return self.name

class Anonymous(AnonymousUserMixin):
	def __init__(self):
		self.name = 'guest'

	def get_id(self):
		return self.name

def admin_required(func):
	@login_required
	def wrapped(*args,**kwargs):
		if current_user.name != "admin":
			return "admin required"
		else:
			f(*args, **kwargs)
	return wrapped


def rights(policy):
	result = {}
	for key, values in policy.items():
		if "guest" in values:
			result[key] = True
			continue
		if current_user.name == "admin":
			result[key] = True
			continue
		for value in values:
			if value[0] == "@" and current_user.name == value[1:]:
				result[key] = True
				break
		else:
			result[key] = False
	return result