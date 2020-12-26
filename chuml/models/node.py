from chuml.utils import db
from chuml.utils.db import Column, Integer, String, \
						relationship, Base, ForeignKey, \
						Boolean

from flask_login import current_user
import time
						
nodes_labels_table = db.Table('nodes_labels', Base.metadata,
	Column('node_id', Integer, ForeignKey('nodes.id')),
	Column('label_id', Integer, ForeignKey('labels.id'))
)

class Node(Base):
	__tablename__ = 'nodes'
	id = Column(Integer, primary_key=True)
	author_id = Column(Integer, ForeignKey("users.id"))
	author = relationship("User")
	access_id = Column(Integer, ForeignKey("access_policies.id"))
	access = relationship("AccessPolicy")
	labels = relationship("Label",
		secondary=nodes_labels_table,
		back_populates="labeling"
	)
	created_timestamp = Column(Integer)
	updated_timestamp = Column(Integer)
	attention         = Column(db.Float, default=0)

	type = Column(String(20))

	__mapper_args__ = {
		'polymorphic_on':type,
		'polymorphic_identity':'node'
	}

	def __init__(self, *args, **kwargs):
		self.author = current_user
		self.created_timestamp = int(time.time())
		self.updated_timestamp = self.created_timestamp
		
		super().__init__(*args, **kwargs)

	def __repr__(self):
		return "<{}>".format(self.type)

	def to_dict(self):
		return {
			"author_id": self.author_id,
			"access_id": self.access_id,
			"labels"   : [l.id for l in self.labels],
			"id"       : self.id,
			"attention": self.attention,
			"created_timestamp": self.created_timestamp,
			"updated_timestamp": self.updated_timestamp,
		}

	def comma_separated_labels(self):
		return ", ".join([label.name for label in self.labels])