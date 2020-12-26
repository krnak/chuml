import json
from chuml.auth import auth
from chuml.search import bookmarks
from chuml.search import labels
from chuml.utils import db
from chuml.search import search

#db.db_path = "../../db"
author = db.query(auth.User).filter_by(name="agi").first()

with open("/home/agi/backups/chuml-20201209/engines.json") as file:
	engines = json.load(file)

for key, data in engines.items():
	e = search.SearchEngine(
		key=key,
		author=author
	)
	if "search" in data:
		e.search = data["search"]
	if "url" in data:
		e.url = data["url"]
	else:
		print("engine without url", key)

	db.add(e)
	db.commit()
	print(key)