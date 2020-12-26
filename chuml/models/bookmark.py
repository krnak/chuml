from chuml.utils import db
from chuml.models import node

class Bookmark(node.Node):
	__tablename__ = "bookmarks"
	id         = db.Column(db.Integer, db.ForeignKey("nodes.id"),
							primary_key=True)
	name       = db.Column(db.String)
	url        = db.Column(db.String)
	note       = db.Column(db.String)
	__mapper_args__ = {
		'polymorphic_identity':'bookmark'
	}

	def __repr__(self):
		return "<Bookmark {}>".format(self.name)

	def to_dict(self):
		return {
			"name": self.name,
			"url" : self.url,
			"note": self.note,
			**super().to_dict()
		}