from flask import Flask, url_for, redirect
from flask_login import LoginManager 

from adresa.adresa import adresa
from search.search import search
from auth.auth import auth
from blog.blog import blog
from storage.storage import storage
from forum.forum import forum
from search.bookmarks import bookmarks
from search.labels import labels

from chuml.utils import db

app = Flask(__name__)
app.register_blueprint(adresa)
app.register_blueprint(search)
app.register_blueprint(auth)
app.register_blueprint(blog)
app.register_blueprint(storage)
app.register_blueprint(forum)
app.register_blueprint(bookmarks)
app.register_blueprint(labels)

app.secret_key = db.load_or_write("sensitive", "app_secret")

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return auth.User(user_id)

@app.route("/")
def index():
	return redirect(url_for("auth.index"))