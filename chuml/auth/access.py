# access.py

from flask_login import current_user
from chuml.utils import crypto

NOTHING = 0
VIEW    = 1
EDIT    = 2
ADMIN   = 3

def admin_required(func):
    @login_required
    def wrapped(*args,**kwargs):
        if current_user.name != "admin":
            return "admin required"
        else:
            func(*args, **kwargs)
    return wrapped

def forbidden_page():
    return "<h1>Access Forbidden</h1>"