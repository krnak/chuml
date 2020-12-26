# node.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint, flash
from flask_login import login_required, current_user
import time

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from chuml.utils import db
from chuml.models import Node
from chuml.models import Label
from chuml.auth import access

nodes_bp = Blueprint('node', __name__,
	url_prefix="/node", static_url_path="static",
	template_folder='templates')

class NodeForm(FlaskForm):
	pass

@nodes_bp.route("/<id>/edit", methods=["POST"])
@login_required
def edit_post(id=0):
	node = db.query(Node).get(id)
	if not node:
		return "node {} not found".format(id)
	
	if access.access(node) < access.EDIT:
		return "access forbidden to node {}".format(id)
	try:
		action = get_arg("action")

		if   action == "remove_label":
			label_name = get_arg("label_name")
			label = db.query(Label).filter_by(
				author=current_user,
				name=label_name,
			).one_or_none()
			node.labels.remove(label)
			db.commit()
			return "success: label removed"
		elif action == "add_label":
			label_name = get_arg("label_name")
			label = db.query(Label).filter_by(
				author=current_user,
				name=label_name,
			).one_or_none()
			if not label:
				label = Label(name=name)
				db.add(label)
				db.commit()
			node.labels.append(label)
			db.commit()
			return "success: label added"
		else:
			return "nothing done"
	except Exception as e:
		print("===== nodes =====")
		print(e)
		print("==================")
		db.rollback()
		return str(e)

def get_arg(name):
	arg = request.form.get(name)
	if not arg:
		raise ValueError("argument `{}` required".format(name))
	return arg

"""
# TEMPLATE
class (labelNode):

	__mapper_args__ = {
		'polymorphic_identity':''
	}
"""
