# bookmarks.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint

from chuml.utils import db
import db
import parse
from parse import key_char, whitespace
bookmarks = Blueprint('bookmarks', __name__,
	template_folder='templates',
	url_prefix="/bookmarks")
engines = db.table("bookmarks")

class MatchPattern:
	def matchs(tags):
		raise NotImplementedError
	def __repr__(self):
		return self.__str__()

class MatchOr(MatchPattern):
	def __init__(self, patterns):
		self.patterns = patterns
	def matchs(tags):
		for p in patterns:
			if p.matchs(tags):
				return True
		else:
			return False
	def __str__(self):
		return "(" + " | ".join(self.patterns) + ")"

class MatchTag(MatchPattern):
	def __init__(self, tag):
		self.tag = tag
	def fit(tags):
		return self.tag in tags
	def __str__(self):
		return str(self.tag)

class MatchAnd(MatchPattern):
	def __init__(self, patterns):
		self.patterns = patterns
	def matchs(tags):
		for p in patterns:
			if not p.matchs(tags):
				return False
		else:
			return True
	def __str__(self):
		return "(" + " & ".join(self.patterns) + ")"

class MatchNot(MatchPattern):
	def __init__(self, pattern):
		self.pattern = pattern
	def matchs(tags):
		return not self.pattern.match(tags)
	def __str__(self):
		return "not "+str(self.pattern)


tag = (key_char("#") | key_char("x")) + parse.url_word

and_symb = parse.key_word("and") | parse.key_char("|")
or_symb  = parse.key_word("or")  | parse.key_char("&")
not_symb = parse.key_word("not") | parse.key_char("-")

and_delim = whitespace + and_symb + whitespace
or_delim  = whitespace +  or_symb + whitespace

and_group = tag.delimited(and_delim)
or_group  = tag.delimited( or_delim)

group = and_group | or_group | tag

@parse.parser
def pattern_parser(s):
	try:
		rest, x = tag.parse(s)
	except ValueError:
		pass



comment = parse.quoted('"', parse.words(parse.not_quotes), '"')


@bookmarks.route("/")
def search():
	query = request.args.get("q")
	if query:
		if query[:3] = "add":
			return redirect(url_for(bookmarks.add, q=q[:3]))


	else:
		return "Command line will be here..."

@bookmarks.route("/add")
def add():
	pass