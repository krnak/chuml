import json
import os

db_path = "../db"
while not os.path.isdir(db_path):
	print("[db] path not found")
	db_path = input("[db] enter db path:")
	

class SyncFile(dict):
	def __init__(self, path):
		self.path = path
		try:
			with open(path) as file:
				dict.__init__(self, json.load(file))
		except FileNotFoundError:
			dict.__init__(self)	

	def commit(self):
		with open(self.path, "w") as file:
			json.dump(self, file, indent=4)

opened_tables = dict()

def table(table_name):
	if table_name in opened_tables:
		return opened_tables[table_name]
	else:
		table = SyncFile("{}/{}.json".format(db_path, table_name))
		table.commit()
		opened_tables[table_name] = table
		return table

def load_or_write(table_name, key):
	"""Pokusi se nacist hodnotu z db. Pokud selze, nacte ji z cmd."""
	table_ref = table(table_name)
	try:
		return table_ref[key]
	except KeyError:
		#value = input(f"Zadej hodnotu \"{key}\" do tabulky \"{table_name}\":")
		value = input("Zadej hodnotu \"{}\" do tabulky \"{}\":".format(key, table_name))
		table_ref[key] = value
		table_ref.commit()
		return value

def log(msg):
	with open(db_path + "/log.txt", "a") as file:
		file.write(msg + "\n")
