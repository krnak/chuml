# labels.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint
from flask_login import login_required, current_user

import time
import json

from chuml.utils import db
from chuml.utils import crypto
from chuml.auth import auth

labels = Blueprint('labels', __name__,
	template_folder='templates',
	url_prefix="/labels")

labels_table = db.table("labels")

@labels.route("/")
@login_required
def search():
	query = request.args.get("q")
	if query:
		if query[:3] == "add":
			return redirect(url_for("labels.add", q=query[3:]))

		# more sophisticated engine is comming
		# label_part = query.split(" ")[0]
		# matched = [label
		#	for label in labels_table.values()
		#	 if label_part in label]
		# matched.sort()
		return "Not implemented." #render_template("bm_results.html",
		#	results=matched,label=label)

	return render_template("labels.html",
		labels=labels_table,rights=auth.rights,
		current_user_name=current_user.name,
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

		internal_add(label, current_user.name, labels)

		return ("Label</br>"
				+'#'+name
				+"</br>with labels: "+str(labels)
				+"</br>added.")
	return "bookmark.add requires argment q"

def internal_add(name,author,labels=None,t=None):
	if t == None:
		t = int(time.time())
	if not labels:
		labels = []
	#if ':' in name:
	#	print(name)

	iid = author+':'+name

	if iid in labels_table.keys():
		label = labels_table[iid]
		label["labels"] = list(
			set(label["labels"]) | set(labels)
		)
		labels_table.commit()
	else:
		label = {
			"name": name,
			"labels": labels,
			"author": author,
			"access_policy": {
				"edit":['@'+author],
				"view":['@'+author]
			},
			"time": t
		}

		labels_table[iid] = label
		labels_table.commit()


def sublabels_of(iid):
	return [k for k,v in labels_table.items()
		if iid in v["labels"]
		and v["name"][0] != '_']

def upperlabels_of(iid):
	return [ lb for lb
				in labels_table[iid]["labels"]
				if lb.split(':')[1][0] != '_']

def signed(label):
	if label["author"] == current_user.name:
		return '#'+label["name"]
	else:
		return '#'+label["author"]+':'+label["name"]
