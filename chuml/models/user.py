from chuml.models.utils import gen_attributes
from chuml.models.node import Node
from chuml.models.primitives import String
from chuml.utils import db
from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin, Node):
	gen_attributes(locals(), {
		"name": String,
		"pasw": String,
		"salt": String,
	})

	def get_id(self):
		return self.id


class Anonymous(AnonymousUserMixin):
	def __init__(self):
		self.name = 'guest'

	def get_id(self):
		return self.name

	def __repr__(self):
		return "<AnonymousUser>"
