# labels.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint, flash
from flask_login import login_required, current_user

import time
import json

from chuml.utils import db
from chuml.utils import crypto
from chuml.auth  import access
from chuml.models import Label

labels = Blueprint('labels', __name__,
	template_folder='templates',
	url_prefix="/label")

@labels.route("/")
@login_required
def index():
	q = request.args.get("q", default="")
	search_set = db.query(Label).filter(
		Label.name.like("%{}%".format(q))
	).all()

	accessible_labels = [ p for p in search_set
						if access.access(p) >= access.VIEW]

	if not accessible_labels:
		return "No labels found."

	if len(accessible_labels) == 1:
		return redirect(url_for("labels.view",
			id=accessible_labels[0].id))

	return render_template("labels.html",
		labels=accessible_labels,
		signed=signed
		)

@labels.route("/add")
@login_required
def add():
	query = request.args.get("q")
	# TODO: add override warning
	if query:
		print("[labels]", query)
		query  = query.split()
		name   = query[0]
		labels = query[1:]

		# TODO: add double dot feature
		labels = [ l for l in db.query(Label).filter_by(author=current_user).all()
			if l.name in labels
		]
		internal_add(name, current_user, labels)

		return ("Label</br>"
				+'#'+name
				+"</br>with labels: "+", ".join(map(signed,labels))
				+"</br>added.")
	return "bookmark.add requires argment q"

#TODO : add under lattest label / mix label

@labels.route("/<id>")
@login_required
def view(id=0):
	label = db.query(Label).get(id)
	if not label:
		flash("Label {} not found.".format(id))
		return redirect(url_for('labels.index'))
	
	if access.access(label) < access.VIEW:
		return access.forbidden_page()

	# TODO: SQL filtering
	labeled = [ i for i in label.labeling
				if access.access(i) >= access.VIEW ]

	bms  = [i for i in labeled if i.type == "bookmark"]
	lbls = [i for i in labeled if i.type == "label"]

	bms.sort( key=lambda x: x.created_timestamp)
	lbls.sort(key=lambda x: x.created_timestamp)

	return render_template("bm_results.html",
		bookmarks=bms,
		label =label,
		labels=lbls,           #VIEW RIGHTS
		backs =label.labels,   #VIEW RIGHTS
		signed=signed
	)


def internal_add(name,author,labels=[],t=None):
	if t == None:
		t = int(time.time())

	if db.query(Label).filter_by(name=name,author=author).all():
		label = db.query(Label).filter_by(name=name,author=author).first()
	else:
		label = Label(
			name=name,
			author=author,
			created_timestamp=t,
			updated_timestamp=t
		)
		db.add(label)

	for l in labels:
		if not l in label.labels:
			label.labels.append(l)
	db.commit()

	return label

def signed(label):
	# .id ==
	if label.author == current_user:
		return '#'+label.name
	else:
		return '#'+label.author.name+':'+label.name

def users_labels():
	return db.query(Label).filter_by(author=current_user).all()
