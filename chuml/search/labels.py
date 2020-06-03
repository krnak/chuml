# labels.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint
import time
import json

from chuml.utils import db
from chuml.utils import crypto

labels = Blueprint('labels', __name__,
	template_folder='templates',
	url_prefix="/labels")

labels_table = db.table("labels")

@labels.route("/")
def search():
	query = request.args.get("q")
	if query:
		if query[:3] == "add":
			return redirect(url_for("labels.add", q=query[3:]))

		# more sophisticated engine is comming
		label_part = query.split(" ")[0]
		matched = [label
			for label in labels_table.values()
			 if label_part in label]
		matched.sort()
		return render_template("bm_results.html",
			results=matched,label=label)

	return render_template("labels.html",
		labels=labels_table.keys())

@labels.route("/add")
def add():
	query = request.args.get("q")
	# TODO: add override warning
	if query:
		print("[labels]", query)
		query  = query.split()
		name   = query[0]
		labels = query[1:] 

		internal_add(label, labels)

		return ("Label</br>"
				+'#'+name
				+"</br>with labels: "+str(labels)
				+"</br>added.")
	return "bookmark.add requires argment q"

def internal_add(name,labels=None,iid=None):
	if not labels:
		labels = ["unlabeled"]
	if name in labels_table.keys():
		label = labels_table[name]
		if iid:
			label["iid"] = iid
		label["labels"] = list(
			set(label["labels"]) | set(labels)
		)
		labels_table.commit()
	else:
		label = {
			"name": name,
			"labels": labels
		}
		if iid:
			label["iid"] = iid

		labels_table[name] = label
		labels_table.commit()


def sublabels_of(label):
	return [lb["name"] for lb in labels_table.values()
		if label in lb["labels"]
		and lb["name"][0] != '_']

def upperlabels_of(label):
	return [ lb for lb
				in labels_table[label]["labels"]
				if lb[0] != '_']
