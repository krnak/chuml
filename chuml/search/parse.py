def no_parse_func():
	raise NotImplementedError
ParserError = ValueError("Parser does not fit.")

"""
def merge(a,b):
	c = a.copy()
	for key in c:
		if key in b:
			c[key] = c[key].merge(b[key])
		else:
			c[key] = b[key]
	return c

class Content:
	def __init__(self, typ):
		self.typ = typ
	def merge(self, other):
		raise NotImplementedError

class AdditiveContent(Content):
	def __init__(self, typ, data):
		super().__init__(self, typ)
		self.data = data
	def merge(self, other):
		return AdditiveContent(self.typ, self.data + other.data)
"""
# decorator
def parser(func):
	def wrapper(*args,**kwargs):
		parse = lambda s: func(*args, s=s, **kwargs)
		return Parser(func=parse)
	return wrapper


class Parser:
	def __init__(self, func=no_parse_func):
		self.parse = func

	@parser
	def __add__(self, other, s):
		rest, x1 = self.parse(s)
		rest, x2 = other.parse(s)
		if   x1 == None:
			return (rest, x2)
		elif x2 == None:
			return (rest, x1)
		else:
			return (rest, x1 + x2)

	@parser
	def __or__(self, other, s):
		try:
			rest, x = self.parse(s)
		except ValueError:	
			rest, x = other.parse(s)
		return (rest, x)

	@parser
	def cycle(self, x, s):
		rest = s
		while True:
			try:
				rest, xx = self.parse(rest)
				x += xx
			except ValueError:
				break
		return (rest, x)

	@parser
	def cycle_some(self, s):
		rest, x = self.parse(s)
		while True:
			try:
				rest, xx = self.parse(rest)
				x += xx
			except ValueError:
				break
		return (rest, x)

	@parser
	def to_list(self, s):
		rest, x = self.parse(s)
		return (rest, [x])

	@parser
	def delimited(self, de, s):
		rest, x = self.parse(s)
		while True:
			try:
				rest, xx = (de + self).parse(rest)
				x += xx
			except ValueError:
				break
		return (rest, x)


@parser
def key_char(char, s):
	if not s or s[0] != char:
		raise ParserError
	else:
		return (s[1:],None)

def quoted(left, middle, right):
	return key_char(left) + middle + key_char(right)

whitespace = key_char(" ").cycle_some()

def keyword(word):
	return sum(key_char(c) for c in word)

@parser
def char(alphabet, s):
	if not s:
		raise ParserError
	if not s[0] in alphabet:
		raise ParserError
	else:
		return (s[1:], AdditiveContent("chars", s[0]))

def word(alphabet):
	return parse_char(alphabet).cycle_some()

def words(alphabet):
	return            parse_word(alphabet).to_list() + \
		(whitespace + parse_word(alphabet).to_list()).cycle()

upper_case  = set("QWERTYUIOPASDFGHJKLZXCVBNM")
lower_case  = set("qwertyuiopasdfghjklzxcvbnm")
digits      = set("0123456789")
url_safe    = set("-_") | upper_case | lower_case | digits
punctuation = set(",.?!,")
symbols     = set("~!@#$%^&*-_=+\\|:;,<.>/?")
parenthesis = set("(){}[]<>")
quotes      = set("'\"")
space       = set([" "])
not_quotes  = symbols | parenthesis | url_safe | space

url_word = word(url_safe)


