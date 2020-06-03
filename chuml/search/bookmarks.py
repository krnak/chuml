# bookmarks.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint
import time
import json

from chuml.utils import db
from chuml.utils import crypto
from chuml.search import labels

bookmarks = Blueprint('bookmarks', __name__,
	template_folder='templates',
	url_prefix="/bookmarks")

table = db.table("bookmarks")

#TODO : add under lattest label / mix label

@bookmarks.route("/")
def search():
	query = request.args.get("q")
	if query:
		if query[:3] == "add":
			return redirect(url_for("bookmarks.add", q=query[3:]))

		# more sophisticated engine is comming
		label = query.split(" ")[0]
		# what if label dont exists?
		matched = [bm
			for  bm   in table.values()
			 if label in bm["labels"]]
		matched.sort(key=lambda x: x["time"])
		return render_template("bm_results.html",
			bookmarks=matched,
			label=label,
			labels=labels.sublabels_of(label),
			backs=labels.upperlabels_of(label)
			)

	return redirect(url_for("search.line"))

@bookmarks.route("/add")
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

def internal_add(name, url, lbs=None, t=None):
	if lbs == None:
		lbs = []
	if t == None:
		t = int(time.time())

	bookmark = {
		"name": name,
		"url" : url,
		"labels": lbs,
		"time": t
	}

	iid = crypto.get_iid(url)

	table[iid] = bookmark
	table.commit()

	for lb in lbs:
		labels.internal_add(lb)
