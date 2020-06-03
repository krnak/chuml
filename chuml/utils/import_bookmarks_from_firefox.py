import json
from chuml.search import bookmarks
from chuml.search import labels

def add_node(node,parrent_name=None):
	name = node["title"]
	if name:
		if parrent_name:
			labels.internal_add(name,[parrent_name])
		else:
			labels.internal_add(name)

	if not "children" in node:
		return

	for c in node["children"]:
		if c["typeCode"] == 2: # node
			add_node(c,name)
		elif c["typeCode"] == 1: # leaf
			add_leaf(c,name)


def add_leaf(leaf, parrent_name):
	name = leaf["title"]
	t    = leaf["lastModified"]//1000
	iid  = leaf["guid"]
	uri  = leaf["uri"]
	if not parrent_name:
		raise ValueError("No parrent name.")

	bookmarks.internal_add(name,uri,[parrent_name,"_from_firefox"],t)

if __name__ == "__main__":
	with open("/home/agi/Downloads/bookmarks-2020-05-21.json") as file:
		firefox = json.load(file)
	add_node(firefox)