from chuml.utils import db
from chuml.models import *

to_export = [Bookmark, Label, Note, SearchEngine, User]#, \
             #Sensitive, User, AccessPolicy, UserAccess]

result = dict()

for model in to_export:
	cont = []
	result[model.__tablename__] = cont
	for obj in db.query(model).all():
		cont.append(obj.to_dict())

import json
with open("dump.json", "w") as file:
	json.dump(result, file)
