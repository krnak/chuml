from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint
from flask_login import current_user

from urllib.parse import quote

from chuml.search import wiki

from chuml.utils import db
from chuml.auth import access
from chuml.models import SearchEngine


search = Blueprint('search', __name__,
	template_folder='templates',
	url_prefix="/search")
#engines = db.table("engines")

def extended_split(string):
	# Split the word according to the spaces,
	# but ignores spaces "inside of quotation marks"
	buff = ""
	in_quotes = False
	words = []
	for char in string + " ": # space adds the last word
		if  char == "\"":
			in_quotes = not in_quotes
		elif char == " " and not in_quotes:
			if buff:
				words.append(buff)
			buff = ""
		else:
			buff += char
	return words


@search.route("/add")
def add():
	if "q" in request.args:
		words = extended_split(request.args.get("q"))
		key,url,search = (words + 3*[""])[:3]
		return redirect(url_for("search.add", key=key,url=url,search=search))

	elif  "key" in request.args and request.args.get("url"):
		key = request.args.get("key")
		if not key.replace(" ","").replace("_","").replace("-","").isalnum():
			return "Invalid key."

		url = request.args.get("url")

		engine = db.query(SearchEngine).filter_by(
			key=key,
			author=current_user
		).one_or_none()
		if engine:
			force = request.args.get("force")
			if not force == "True":
				return render_template("add.html",
					caption = "{key} already points at {url}".format(
						key=key,
						url=engine.url
					),
					key     = request.args.get("key",""),
					url     = request.args.get("url",""),
					search  = request.args.get("search",""),
					force   = "True",
					button  = "Override"
				)
			else:
				engine.url = url
				engine.search = request.args.get("search")
				db.commit()
		else:
			engine = SearchEngine(
				url=url,
				key=key,
				search=request.args.get("search"),
			)
			db.add(engine)
			db.commit()

		return """
				<b>{key}</b> -> {url}
				<br/> added <br/>
				<a href="{url}">back</a>
			   """.format(
					key=key,
					url=engine.url
				)
	else:
		return render_template("add.html",
			caption = "example search: https://www.google.com/search?q={query}",
			key     = request.args.get("key",""),
			url     = request.args.get("url",""),
			search  = request.args.get("search",""),
			force   = "",
			button  = "Submit"
		)

@search.route("/")
def line():
	query = request.args.get("q")
	if not query:
		return render_template("search.html")

	words = query.split()
	keyword = words[0]
	if db.query(SearchEngine).filter_by(
			key=keyword,
			author=current_user
		).all():
		keyword = ""
		engine = None
		exp = None
		for i,word in enumerate(words):
			if db.query(SearchEngine).filter_by(
				key=keyword+word,
				author=current_user).all():
				keyword += word
				engine = db.query(SearchEngine).filter_by(
					key=keyword,
					author=current_user
				).first()
			else:
				exp = " ".join(words[i:])
		
		if not exp:
			return redirect(engine.url)

		if engine.search:
			return redirect(
				engine.search.format(query=quote(exp))
			)
		"""
		elif keyword == "add":
			exp = " ".join(query.split()[1:])
		return redirect(url_for("search.add",q=exp))
		elif keyword == "bm":
			exp = " ".join(query.split()[1:])
			return redirect(url_for("bookmarks.search",q=exp))
		elif keyword == "lb":
			exp = " ".join(query.split()[1:])
			return redirect(url_for("labels.search",q=exp))
		elif keyword == "a":
			blogid = query.split(" ")[1]
			line = " ".join(query.split()[2:])
			return redirect(url_for("blog.append",id=blogid,line=line))"""

	return redirect("https://google.com/search?q="+query)

	
	# search
	#if engine_name == "wiki":
	#	return wiki.search(exp)
