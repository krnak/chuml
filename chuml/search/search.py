from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint

from urllib.parse import quote

from . import wiki

from chuml.utils import db


search = Blueprint('search', __name__,
	template_folder='templates',
	url_prefix="/search")
engines = db.table("engines")

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
		if key in engines.keys():
			force = request.args.get("force")
			if not force == "True":
				return render_template("add.html",
					caption = "{key} already points at {url}".format(
						key=key,
						url=engines[key]["url"]
					),
					key     = request.args.get("key",""),
					url     = request.args.get("url",""),
					search  = request.args.get("search",""),
					force   = "True",
					button  = "Override"
				)
		engines[key] = dict()
		engines[key]["url"] = url

		search = request.args.get("search")
		if search:
			engines[key]["search"] = search

		engines.commit()

		return """
				<b>{key}</b> -> {url}
				<br/> added <br/>
				<a href="{url}">back</a>
			   """.format(
					key=key,
					url=engines[key]["url"]
				)
	else:
		return render_template("add.html",
			caption = "key url search{query}",
			key     = request.args.get("key",""),
			url     = request.args.get("url",""),
			search  = request.args.get("search",""),
			force   = "",
			button  = "Submit"
		)

@search.route("/")
def line():
	query = request.args.get("q")
	if query:
		words = query.split()
		keyword = words[0]
		if keyword in engines:
			i = 1
			while i < len(words) and (keyword +  " " + words[i]) in engines:
				keyword += " " + words[i]
				i += 1
			exp = " ".join(words[i:])
			engine_name = keyword
			engine = engines[keyword]
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
			return redirect(url_for("blog.append",id=blogid,line=line))
		else:
			exp = query
			engine_name = "g"
			engine = engines[engine_name]
		
		# just url
		if not exp:
			return redirect(engine["url"])
		
		# search
		if engine_name == "wiki":
			return wiki.search(exp)
		if not "search" in engine:
			exp = query
			engine_name = "g"
			engine = engines[engine_name]
			
		return redirect(
			engine["search"].format(query=quote(exp))
		)
	else:
		return render_template("search.html")