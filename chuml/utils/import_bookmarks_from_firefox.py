import json
from chuml.auth import auth
from chuml.search import bookmarks
from chuml.search import labels
from chuml.utils import db

#db.db_path = "../../db"
author = db.query(auth.User).filter_by(name="agi").first()
from_firefox_label = labels.internal_add("_from_firefox", author)

def add_node(node,parrent=None):
	label = None
	name = node["title"].replace(' ', '_')
	if name:
		t    = node["lastModified"]//1000
		if parrent:
			label = labels.internal_add(name,author,[parrent],t=t)
		else:
			label = labels.internal_add(name,author,t=t)
	else:
		raise ValueError("no title")

	print("======",label.__repr__(),"=======")

	if not "children" in node:
		return

	for c in node["children"]:
		if c["typeCode"] == 2: # node
			add_node(c,label)
		elif c["typeCode"] == 1: # leaf
			add_leaf(c,label)


def add_leaf(leaf, parrent):
	name = leaf["title"]
	t    = leaf["lastModified"]//1000
	iid  = leaf["guid"]
	uri  = leaf["uri"]
	if not parrent:
		raise ValueError("No parrent.")

	print("====== adding bm ", [name,uri,author,[parrent,from_firefox_label],t])
	bookmarks.internal_add(name,uri,author,[parrent,from_firefox_label],t)

if __name__ == "__main__":
	with open("/home/agi/Downloads/bookmarks-2020-05-21.json") as file:
		firefox = json.load(file)
	add_node(firefox)