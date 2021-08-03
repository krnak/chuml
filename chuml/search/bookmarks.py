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

@bookmarks.route("/<id>/edit", methods=["GET"])
@login_required
def edit_get(id=0):
	bm = db.query(Bookmark).get(id)
	if not bm:
		flash("Bookmark {} not found.".format(id))
		return redirect(url_for('labels.index'))
	
	if access.access(bm) < access.EDIT:
		return access.forbidden_page()

	return render_template("edit_bookmark.html",
		bm=bm)

@bookmarks.route("/<id>/edit", methods=["POST"])
@login_required
def edit_post(id=0):
	bm = db.query(Bookmark).get(id)
	if not bm:
		flash("Bookmark {} not found.".format(id))
		return redirect(url_for('labels.index'))
	
	if access.access(bm) < access.EDIT:
		return access.forbidden_page()

	try:
		action = get_arg("action")
		if   action == "set_name":
			bm.name = get_arg("name")
			db.commit()
			return "success: name set"
		elif action == "set_url":
			bm.url = get_arg("url")
			db.commit()
			return "success: url set"
		elif action == "delete":
			bm.labels.clear()
			db.delete(bm)
			db.commit()
			return "success: deleted"
		else:
			return "nothing done"
	except Exception as e:
		print("===== bookmarks =====")
		print(e)
		print("==================")
		db.rollback()
		return str(e)

def get_arg(name):
	arg = request.form.get(name)
	if not arg:
		raise ValueError("argument `{}` required".format(name))
	return arg


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
