# bookmarks.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint
from flask_login import login_required, current_user

import time
import json

from chuml.utils import db
from chuml.utils import crypto
from chuml.search import labels
from auth.auth import rights

bookmarks = Blueprint('bookmarks', __name__,
	template_folder='templates',
	url_prefix="/bookmarks")

table = db.table("bookmarks")
labels_table = db.table("labels")

#TODO : add under lattest label / mix label
iids_to_labels = lambda x : [db.table("labels")[iid]
							 for iid in x]
@bookmarks.route("/")
@login_required
def search():
	query = request.args.get("q")
	if query:
		if query[:3] == "add":
			return redirect(url_for("bookmarks.add", q=query[3:]))

		# more sophisticated engine is comming
		# how about other users???
		label = current_user.name+':'+query.split(" ")[0]
		if not label in labels_table:
			return "Label #" + label + " not found."

		matched = [bm
			for  bm   in table.values()
			 if label in bm["labels"]]
		matched.sort(key=lambda x: x["time"])

		return render_template("bm_results.html",
			bookmarks=matched,
			label=db.table("labels")[label],
			labels=iids_to_labels(labels.sublabels_of(label)),
			backs=iids_to_labels(labels.upperlabels_of(label)),
			rights=rights,
			signed=labels.signed
		)

	return redirect(url_for("search.line"))

@bookmarks.route("/add")
@login_required
def add():
	query = request.args.get("q")
	# TODO: add override warning
	if query:
		query = query.split()
		print("[bookmarks]", query)
		url   = query.pop()
		if url[:4] != "http":
			url = "https://" + url
		labels = [label[1:] for label in query if label[0] == '#']
		words = [word  for word in query if word[0] != '#']
		name = " ".join(words)

		internal_add(name,url,labels)

		return ("Bookmark</br>"
				+name+"-><a href="+url+">"+url+"</a>"
				+"</br>with labels: "+str(labels)
				+"</br>added.")
	return "bookmark.add requires argment q"

def internal_add(name, url, author, lbs=None, t=None):
	if lbs == None:
		lbs = []
	if t == None:
		t = int(time.time())

	bookmark = {
		"name": name,
		"url" : url,
		"labels": lbs,
		"time": t,
		"author": author,
		"access_policy": {
			"edit":['@'+author],
			"view":['@'+author]
		}
	}

	iid = crypto.get_iid(url+author+name)

	table[iid] = bookmark
	table.commit()
