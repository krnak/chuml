from chuml.utils import db
from chuml.models import Sensitive

def load_or_write(key):
	item = db.query(Sensitive).get(key)
	if not item:
		value = input("Enter " + key + ":")
		db.add(Sensitive(key=key,value=value))
		db.commit()
	else:
		value = item.value
		
	return value

