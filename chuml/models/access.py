from chuml.utils import db
from chuml.models.primitives import Integer, String
from chuml.models.utils import gen_attributes
from chuml.models.user import User
from chuml.models.node import Node
from chuml.auth import access

from flask import request
from flask_login import current_user

# user access = (user, node) -> level
# link access = (link, node) -> level
# public access = node -> level


class Access(db.Base):
    __abstract__ = True  # https://stackoverflow.com/a/18675245/5802474
    gen_attributes(locals(), {
        "node": Node,
        "can": Integer,
    })

    def condition(self):
        raise NotImplementedError

    def allows(self):
        if self.condition():
            return self.can
        else:
            return access.NOTHING


class UserAccess(Access, Node):
    gen_attributes(locals(), {
        "user": User,
    })

    def condition(self):
        return self.user == current_user


class LinkAccess(Access, Node):
    gen_attributes(locals(), {
        "secret": String,
    })

    def condition(self):
        self.secret == request.args.get("secret")


class PublicAccess(Access, Node):
    def condition(self):
        return True
