from chuml.utils import db
from chuml.models import node

class Label(node.Node):
	__tablename__ = "labels"
	id         = db.Column(db.Integer, db.ForeignKey("nodes.id"), primary_key=True)
	name       = db.Column(db.String)
	labeling   = db.relationship("Node",
		secondary=node.nodes_labels_table,
		back_populates="labels")
	note       = db.Column(db.String)

	__mapper_args__ = {
		'polymorphic_identity':'label'
	}

	def __repr__(self):
		return "<Label {}>".format(self.name)

	def to_dict(self):
		return {
			"name": self.name,
			"note": self.note,
			**super().to_dict()
		}