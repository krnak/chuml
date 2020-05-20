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
		tag = query.split(" ")[0]
		matched = [(bm["time"], bm)
			for bm  in table.values()
			 if tag in bm["tags"]]
		matched.sort()
		matched = [bm[1] for bm in matched]
		return render_template("bm_results.html",
			results=matched,tag=tag)

	return redirect(url_for("search.line"))

@bookmarks.route("/add")
def add():
	query = request.args.get("q")
	# TODO: add override warning
	if query:
		query = query.split()
		print("[bookmarks]", query)
		url   = query.pop()
		tags = [tag[1:] for tag in query if tag[0] == '#']
		words = [word  for word in query if word[0] != '#']
		name = " ".join(words)

		bookmark = {
			"name": name,
			"url" : url,
			"tags": tags,
			"time": int(time.time())
		}
		iid = crypto.get_iid(url)

		table[iid] = bookmark
		table.commit()
		return ("Bookmark</br>"
				+name+"->"+url
				+"</br>with tags: "+str(tags)
				+"</br>added.")
	return "bookmark.add requires argment q"