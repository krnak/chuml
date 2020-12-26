from chuml.utils import db
from chuml.utils.db import Column, Integer, String, Boolean, ForeignKey
from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin,db.Base):
	__tablename__ = "users"
	id   = Column(Integer, primary_key=True)
	name = Column(String, unique=True)
	pasw = Column(String)
	salt = Column(String)
	
	email = Column(String)
	email_verified = Column(Boolean)

	def get_id(self):
		return self.id

	def __repr__(self):
		return "<User {}>".format(self.name)

	def to_dict(self):
		return {
			"id":    self.id,
			"name":  self.name,
			"pasw":  self.pasw,
			"salt":  self.salt,
			"email": self.email,
			"email_verified": self.email_verified
		}


class Anonymous(AnonymousUserMixin):
	def __init__(self):
		self.name = 'guest'

	def get_id(self):
		return self.name

	def __repr__(self):
		return "<AnonymousUser>"