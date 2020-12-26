from flask import Flask, url_for, redirect
from flask_login import LoginManager, current_user 

from chuml.utils import db
from chuml.utils import sensitive
from chuml.models import User, Anonymous
from chuml.core import config

app = Flask(__name__)

#from adresa.adresa import adresa
#app.register_blueprint(adresa)

print("blueprint notes")
from chuml.notes import notes
app.register_blueprint(notes.notes)

print("blueprint search")
from chuml.search import search
app.register_blueprint(search.search)

print("blueprint auth")
from chuml.auth import auth
app.register_blueprint(auth.auth)

#from storage.storage import storage
#app.register_blueprint(storage)

#from forum.forum import forum
#app.register_blueprint(forum)

print("blueprint labels")
from chuml.search import labels
app.register_blueprint(labels.labels)

print("blueprint bookmarks")
from chuml.search import bookmarks
app.register_blueprint(bookmarks.bookmarks)

print("blueprint nodes")
from chuml.utils import nodes
app.register_blueprint(nodes.nodes_bp)

db.init()
app.secret_key = sensitive.load_or_write("secret_key")

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.anonymous_user = Anonymous
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return db.query(User).get(user_id)

@app.route("/")
def index():
	return redirect(url_for("auth.index"))

def users_labels():
    return '[' + ",".join(['"' + label.name + '"'
    	for label in labels.users_labels()]) + ']'

app.jinja_env.globals.update(users_labels=users_labels)

from chuml.auth import access
def can_view(node):
	return access.access(node) >= access.VIEW

app.jinja_env.globals.update(can_view=can_view)

def can_edit(node):
	return access.access(node) >= access.EDIT

app.jinja_env.globals.update(can_edit=can_edit)

# create admin
if not db.query(User).filter_by(name="admin").one_or_none():
	auth.add_user("admin", config.admin_pasw)

# create guest
if not db.query(User).filter_by(name="guest").one_or_none():
	auth.add_user("guest", config.guest_pasw)


