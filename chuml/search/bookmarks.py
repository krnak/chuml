# bookmarks.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint
import time
import json

from chuml.utils import db
from chuml.utils import crypto

bookmarks = Blueprint('bookmarks', __name__,
	template_folder='templates',
	url_prefix="/bookmarks")

table = db.table("bookmarks")

@bookmarks.route("/")
def search():
	query = request.args.get("q")
	if query:
		if query[:3] == "add":
			return redirect(url_for("bookmarks.add", q=query[3:]))

		# more sophisticated engine is comming
		label = query.split(" ")[0]
		matched = [(bm["time"], bm)
			for bm  in table.values()
			 if label in bm["labels"]]
		matched.sort()
		matched = [bm[1] for bm in matched]
		return render_template("bm_results.html",
			results=matched,label=label)

	return render_template("labels.html",
		labels=all_labels())

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

		bookmark = {
			"name": name,
			"url" : url,
			"labels": labels,
			"time": int(time.time())
		}
		iid = crypto.get_iid(url)

		table[iid] = bookmark
		table.commit()
		return ("Bookmark</br>"
				+name+"-><a href="+url+">"+url+"</a>"
				+"</br>with labels: "+str(labels)
				+"</br>added.")
	return "bookmark.add requires argment q"

def all_labels():
	labels = set()
	for bm in table.values():
		for label in bm["labels"]:
			labels.add(label)
	return list(labels)