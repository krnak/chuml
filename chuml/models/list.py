from chuml.utils import db
from chuml.models import node

lists_nodes_table = db.Table('lists_nodes', db.Base.metadata,
    db.Column('list_id', db.Integer, db.ForeignKey('lists.id')),
    db.Column('node_id', db.Integer, db.ForeignKey('nodes.id')),
)

class List(node.Node):
    # TODO: ordering
    items = db.relationship("Node",
        secondary=lists_nodes_table,
        #back_populates="listed_on"
    )

    # name

    def to_dict(self):
        return {
            "items": [node.id for node in self.items],
            **super().to_dict()
        }

    def render_view(self):
        r = "<ul>"
        for node in self.items:
            r += f"<li>{node.render_view()}</li>"
        r += "</ul>"

    def render_edit(self):
        # TODO: reorder
        r = "<ul>"
        for node in self.items:
            r += f"<li>{node.render_edit()} <a href=/mesh/{self.id}/edit?op=remove&node={node.id}> remove </a></li>"
        r += "</ul>"

    @helpers.with_arg("op")
    @helpers.with_node("node", Node)
    def update(self, op, node):
        if op == "append":
            self.items.append(node)
            db.commit()

        if op == "remove":
            try:
                self.items.remove(node)
                # TODO: gc ??
                db.commit()
            except:
                pass
