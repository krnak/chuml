from chuml.utils import db
from chuml.utils.db import Column, Integer, String
from chuml.models import node

class SearchEngine(node.Node):
	__tablename__ = "search_engines"
	id     = Column(Integer, db.ForeignKey("nodes.id"), primary_key=True)
	key    = Column(String)
	url    = Column(String)
	search = Column(String)
	note   = Column(String)

	__mapper_args__ = {
		'polymorphic_identity':'search_engine'
	}

	def to_dict(self):
		return {
			"key":    self.key,
			"url":    self.url,
			"search": self.search,
			"note":   self.note,
			**super().to_dict()
		}