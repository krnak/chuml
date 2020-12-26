from chuml.utils import db
from chuml.models import node

class Note(node.Node):
    __tablename__ = "notes"
    id = db.Column(db.Integer, db.ForeignKey("nodes.id"), primary_key=True)
    name = db.Column(db.String)
    text = db.Column(db.Text)#, defaut="")
    
    __mapper_args__ = {
        'polymorphic_identity':'note'
    }

    def title(self):
        head = self.text.split("\n")[0]
        if head[0] == '#':
            head = head[1:]
        if head[0] == ' ':
            head = head[1:]
        return head

    def __repr__(self):
        return "<Note {}>".format(self.name)

    def to_dict(self):
        return {
            "name": self.name,
            "text": self.text,
            **super().to_dict()
        }