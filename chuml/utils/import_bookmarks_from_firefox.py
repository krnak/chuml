import json
from chuml.search import bookmarks
from chuml.search import labels
import db

#db.db_path = "../../db"
author = "agi"

def add_node(node,parrent_name=None):
	name = node["title"].replace(' ', '_')
	if name:
		t    = node["lastModified"]//1000
		if parrent_name:
			labels.internal_add(name,author,[author+':'+parrent_name],t=t)
		else:
			labels.internal_add(name,author,t=t)

	if not "children" in node:
		return
	if ':' in name:
		print(name)
	for c in node["children"]:
		if c["typeCode"] == 2: # node
			add_node(c,name)
		elif c["typeCode"] == 1: # leaf
			add_leaf(c,name)


def add_leaf(leaf, parrent_name):
	name = leaf["title"].replace(' ', '_')
	t    = leaf["lastModified"]//1000
	iid  = leaf["guid"]
	uri  = leaf["uri"]
	if not parrent_name:
		raise ValueError("No parrent name.")

	bookmarks.internal_add(name,uri,author,[author+':'+parrent_name,author+":_from_firefox"],t)

if __name__ == "__main__":
	labels.internal_add("_from_firefox",author)
	with open("/home/agi/Downloads/bookmarks-2020-05-21.json") as file:
		firefox = json.load(file)
	add_node(firefox)