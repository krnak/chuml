from chuml.utils import db
from chuml.models import node, gen_attributes
from chuml.models.primitives import String


class Label(node.Node):
    gen_attributes(locals(), {
        "name": String,
    })

    labeling = db.relationship("Node",
        secondary=node.nodes_labels_table,
        back_populates="labels",
    )

    def search(self, word):
        return word in ('#' + str(self.name))

    def render_view(self):
        return f"<div style=\"background: gray; margin: 1px 1px 1px 1px;\">{self.name}</div>"