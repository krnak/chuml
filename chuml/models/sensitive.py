from chuml.utils import db

class Sensitive(db.Base):
	__tablename__ = "sensitive"
	key = db.Column(db.String, primary_key=True)
	value = db.Column(db.String)