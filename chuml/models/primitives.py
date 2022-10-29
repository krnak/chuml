from chuml.utils import db
from chuml import models

class PrimitiveType:
    convert = None

    def __str__(self):
        return str(self.inner)

    def to_dict(self):
        return {
            "inner": self.inner,
            **super().to_dict(),
        }

    def render_view(self):
        return str(self.inner)

    def render_edit(self):  # TODO: use POST ???
        return f"""
            <form method="GET" action="/node/{self.id}/edit">
                <input type="hidden" name="op" value="set">
                <input type="text" name="value" value="{self}">
                <button type="submit">save</button>
            </form>
        """

    @models.with_arg("op", required=True)
    @models.with_arg("value", required=True)
    def update(self, op, value):
        if op == "set":
            try:
                self.inner = self.__class__.convert(value)
                db.commit()
            except ValueError:
                pass

class String(models.Node, PrimitiveType):
    inner = db.Column(db.String)
    convert = str

class Integer(models.Node, PrimitiveType):
    inner = db.Column(db.Integer)
    convert = int

class Float(models.Node, PrimitiveType):
    inner = db.Column(db.String)
    convert = float

class Boolean(models.Node, PrimitiveType):
    inner = db.Column(db.Boolean)
    convert = lambda x: x == "true"

class Text(models.Node, PrimitiveType):
    inner = db.Column(db.Text)
    convert = str