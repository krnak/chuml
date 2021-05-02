from chuml.utils import db
from chuml.utils.db import Column, Integer, String, Boolean, ForeignKey
from chuml.models import user


class UserInfo(db.Base):
    user_id = Column(Integer, primary_key=True)
    user = db.relationship("User")
