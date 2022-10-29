# bookmarks.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint
from flask_login import login_required, current_user

import time
import json
from bs4 import BeautifulSoup
import requests

from chuml.utils import db
from chuml.utils import crypto
from chuml.search import labels
from chuml.auth import access
from chuml.models import Bookmark, Label

bookmarks = Blueprint('bookmarks', __name__,
	template_folder='templates',
	url_prefix="/bookmark")

#table = db.table("bookmarks")
#labels_table = db.table("labels")

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
			url = "http://" + url
		label_name  = query[0]
		words       = query[1:]
		name = " ".join(words)
		if not name:
			name = get_page_title(url)

		label = db.query(Label).filter_by(
			name=label_name,
			author=current_user
		).one_or_none()
		if not label:
			label = labels.internal_add(label_name, current_user)

		internal_add(name,url,current_user,[label])

		return ("Bookmark</br>"
				+"<b>"+name+"</b> -> <a href="+url+">"+url+"</a>"
				+"</br>with label <b>"+label_name+"</b>"
				+"</br>added.")

	return "bookmark.add requires argment q"

def internal_add(name, url, author, lbls=[], t=None):
	if t == None:
		t = int(time.time())
	
	bm = Bookmark(
		name=name,
		url=url,
		created_timestamp=t,
		updated_timestamp=t,
		author=author
	)

	for label in lbls:
		bm.labels.append(label)

	print("======",bm.to_dict())
	print("======", type(bm.labels))
	db.add(bm)
	db.commit()
	return bm

def get_page_title(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text)
	return soup.title.string
