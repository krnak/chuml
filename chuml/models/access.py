from chuml.utils import db
from chuml.utils.db import Column, Integer, String, Boolean, ForeignKey

class UserAccess(db.Base):
	__tablename__ = "user_access"
	user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
	access_policy_id = Column(Integer, ForeignKey("access_policies.id"), primary_key=True)
	user_can = Column(Integer)

	user = db.relationship("User",foreign_keys=[user_id])
	access_policy = db.relationship("AccessPolicy", foreign_keys=[access_policy_id])


class AccessPolicy(db.Base):
	__tablename__ = "access_policies"
	id = Column(Integer, primary_key=True)
	secret = Column(String)
	with_secret_can = Column(Integer)
	public_can = Column(Integer)
	individuals = db.relationship("UserAccess")

	def __repr__(self):
		return "<AccessPolicy public={} link={} individuals={}>".format(
			self.public_can, self.with_secret_can,
			str([(ua.user.name,ua.user_can) for ua in self.individuals]))