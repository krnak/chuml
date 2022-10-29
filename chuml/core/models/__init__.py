from chuml.utils import db
from .db import Column, Integer, String, \
                        relationship, Base, ForeignKey, \
                        Boolean, Float,
                        gen_attributes, snakized

nodes_labels_table = db.Table('nodes_labels', Base.metadata,
    Column('node_id', Integer, ForeignKey('nodes.id')),
    Column('label_id', Integer, ForeignKey('labels.id'))
)

class Node(Base):
    type = Column(String(20))

    @db.declared_attr
    def id(cls):
        if cls.__name__ == "Node":
            return Column(Integer, primary_key=True)
        else:
            return Column(Integer, ForeignKey("nodes.id"), primary_key=True)

    @db.declared_attr
    def __mapper_args__(cls):
        if cls.__name__ == 'Node':
            return {
                "polymorphic_on": cls.type,
                "polymorphic_identity": "node"
            }
        else:
            return {"polymorphic_identity": snakized(cls.__name__)}

    @db.declared_attr
    def __tablename__(cls):
        return snakized(cls.__name__) + "s"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db.commit()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    """
    def to_dict(self):
        raise NotImplementedError  # TODO

        result = dict()
        result["id"] = self.id
        for key in self.__class__.primitive_attributes:
            result[key] = getattr(self, key)
        for key in self.__class__.pointer_attributes:
            result[key+"_id"] = getattr(self, key+"_id")
        if self.__class__ != Node:
            result.update(super().to_dict())

        # TODO: relationships
        return result
    """

    """
    def render_view(self):
        return self.__repr__()

    def render_edit(self):
        return self.render_view() + "(edit)"
    """

    """
    def render_view(self):
        lines = []
        for attr in self.__class__.attributes:
            value = getattr(self, attr)
            lines.append(f"{attr}: {value.render_view()}</ br>")
        return f"<div>{''.join(lines)}</div>"

    def render_edit(self):
        lines = []
        for attr in self.__class__.attributes:
            value = getattr(self, attr)
            lines.append(f"{attr}: {value.render_edit()}</ br>")
        return f"<div>{''.join(lines)}</div>"

    def update(self, op):
        pass
    """

    """
    def search(self, word):
        return False
    """

    """
    def access(self):
        if current_user.name == "admin":
            return ADMIN

        #if current_user == self.author:
        #    return ADMIN  # TODO: depricate ???

        return max(a.allows() for a in self.accesses)
    """

class NodeDecorator(Base):
    id =  Column(Integer, ForeignKey("nodes.id"), primary_key=True)
    __abstract__ = True

    @db.declared_attr
    def __tablename__(cls):
        return snakized(cls.__name__) + "s"
