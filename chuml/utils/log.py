from chuml.utils import db
import time

class Log(db.Base):
	__tablename__ = "logs"
	id = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.Integer)
	text = db.Column(db.Text)

def log(text):
	db.add(Log(text=text,time=int(time.time())))
	db.commit()
