# access.py

from flask import request
from flask_login import current_user

from chuml.utils import crypto
from chuml.utils import db
from chuml.models import AccessPolicy, UserAccess

NOTHING = 0
VIEW    = 1
EDIT    = 2
ADMIN   = 3

def get_self_access_policy():
	ap = AccessPolicy(
		secret=crypto.get_random_secret(),
		with_secret_can=NOTHING,
		public_can=NOTHING
	)
	db.add(ap)
	db.commit()

	ua = UserAccess(
		user_id=current_user.id,
		access_policy_id=ap.id,
		user_can=ADMIN
	)
	ap.individuals.append(ua)
	db.add(ua)
	db.commit()
	return ap

def admin_required(func):
	@login_required
	def wrapped(*args,**kwargs):
		if current_user.name != "admin":
			return "admin required"
		else:
			f(*args, **kwargs)
	return wrapped

def access(chuml_node):
	if current_user.name == "admin":
		return ADMIN
	if current_user == chuml_node.author:
		return ADMIN
	policy = chuml_node.access
	if policy == None:
		return NOTHING
	# public share
	public_access = policy.public_can

	# link share
	secret = request.args.get("secret")
	if secret == policy.secret:
		link_access = policy.with_secret_can
	else:
		link_access = NOTHING

	# individual share

	user_access = db.query(UserAccess).get({
		"user_id": current_user.id,
		"access_policy_id": policy.id
	})
	if user_access:
		individual_access = user_access.user_can
	else:
		individual_access = NOTHING

	return max(public_access, link_access, individual_access)

def forbidden_page():
	return "<h1>Access Forbidden</h1>"