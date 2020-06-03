# storage.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint, flash, abort, \
				  send_from_directory

from chuml.utils import db
from chuml.auth import auth
from chuml.utils import crypto
from flask_login import current_user, login_required

storage = Blueprint('storage', __name__,
	#template_filepath='templates',
	url_prefix='/storage',
	template_folder='templates',
	static_folder="../db/storage")
files_meta = db.table('files_meta')
root = "../db/storage/"

@storage.route('/')
def search():
	return """
	<form action="/storage/upload">
		<input type="submit" value="Upload" />
	</form> Search..."""

@storage.route("/upload", methods=['GET', 'POST'])
def upload():
	if not current_user.is_authenticated:
		print("need to login, then ", request.url)
		return redirect(url_for("auth.login", redirect=request.url))

	if request.method == 'POST':
		if 'file' not in request.files:
			#flash('No file part')
			#return redirect(request.url)
			return 'No file part'

		file = request.files['file']
		filename = file.filename
		if filename == '' or not file:
			#flash('No selected file')
			#return redirect(request.url)
			return "No selected file"

		if not secure_filename(filename):
			return filename + " is invalid filename"

		filepath = request.args.get("filepath", "")
		if filepath and not secure_path(filepath):
			return filepath + " is invalid filepathname"

		path = (filepath + "/" if filepath else "") + filename

		if path in files_meta:
			return path + " already exists."

		file.save(root + path)
		
		can_edit = set(filter("".__ne__,
		request.args.get("edit", "").split(" ")))

		can_view = set(filter("".__ne__,
			request.args.get("view", "").split(" "))).union(can_edit)

		can_edit.add("@" + current_user.name)
		files_meta[path] = {
			"author": current_user.name,
			"acces_policy": {
				"view": list(can_view),
				"edit": list(can_edit)
			}
		}
		files_meta.commit()

		return path + " uploaded."

	else: return '''
	<!doctype html>
	<title>Upload</title>
	<h1>Upload</h1>
	<form method="post" enctype="multipart/form-data">
		<input type="file" name="file">
		<table>
			<tbody>
				<tr>
					<td>Filepath:</td>
					<td><input type="text" name="filepath"></td>
				</tr>
				<tr>
					<td>Can edit:</td>
					<td><input type="text" name="edit"></td>
				</tr>
				<tr>
					<td>Can view:</td>
					<td><input type="text" name="view"></td>
				</tr>
			</tbody>
		</table>
		<input type="submit" value="Upload">
	</form>
	'''

@storage.route('/video')
def video():
	query = request.args.get("q")
	if not query:
		return "q argument required."

	return render_template("video.html", path=query) 

@storage.route('/', defaults={'path': ''})
@storage.route('/<path:path>')
def download(path):
	filename = path.split("/")[-1]
	if not secure_filename(filename):
		return filename + "is invalid filename"
	filepath = "/".join(path.split("/")[:-1])
	if filepath:
		if not secure_path(filepath):
			return path + " is invalid path"

	#if not path in files_meta:
	#	return filepath + " does not exist"

	#access = auth.rights(current_user,
	#	files_meta[path]["access_policy"])
	#if not access["view"]:
	#	return "access denied"

	show = request.args.get("show")=="True"

	try:
		return send_from_directory(
			root + filepath, filename, as_attachment=(not show))
	except FileNotFoundError:
		abort(404)

def secure_path(path):
	for filepath in path.split("/"):
		if not pythonic_name(filepath):
			return False
	else:
		return True

def secure_filename(filename):
	filtered = filename.replace("_","").replace(".","")
	return filtered and filtered.isalnum() 

def pythonic_name(name):
	return len(name) > 0 and name.replace("_","").isalnum()
