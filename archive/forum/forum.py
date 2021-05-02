from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint, jsonify

from urllib.parse import quote
import json

from chuml.utils import crypto
from chuml.utils import db

forum = Blueprint('forum', __name__,
	template_folder='templates',
	url_prefix="/forum")

posts = db.table("posts")
secret = crypto.derive_secret("forum")
print("[forum] secret:", secret)
print("[forum] link: https://flask.krnak.cz/forum?secret="+secret)

@forum.route("/feed", methods=['POST', 'GET'])
@crypto.require_secret(secret)
def feed():
	try:
		m = request.get_json()
	except:
		print("some bad JSON received")

	print("[forum] received msg", m["id"])

	posts[m["id"]] = m
	posts.commit()

	return "ACK"

@forum.route("/get")
@crypto.require_secret(secret)
def get():
	if "t" in request.args:
		time = request.args.get("t", type=int)
		update = [m for m in posts.values()
		             if m["time"] > time]
		if update:
			minimum = update[0]
			for m in update:
				if m["time"] < minimum["time"]:
					minimum = m
			return jsonify(minimum)
		else:
			return jsonify({"time":time})
	else:
		return "This requires parametr t."

@forum.route("/")
@crypto.require_secret(secret)
def board():
	return render_template("forum.html")

def render_msg(m):
	# citation
	return """
	<div>
		<p>{name}:</p>
		{text}
	</div>
	""".format(**m)

