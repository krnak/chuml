# blog.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint, flash
from markdown import markdown

from flask_login import current_user, login_required

from chuml.utils import db
from chuml.auth import auth

blog = Blueprint('blog', __name__,
    template_folder='templates',
    url_prefix='/blog')
blogs = db.table('blog')

@blog.route('/')
def index():
    blogid = request.args.get("id")
    if blogid and blogid.isalnum() and current_user.is_authenticated:
        if not blogid in blogs:
            can_edit = set(filter("".__ne__,
            request.args.get("edit", "").split(" ")))

            can_view = set(filter("".__ne__,
                request.args.get("view", "").split(" "))).union(can_edit)

            can_edit.add("@" + current_user.name)
            blogs[blogid] = {
                "text": "",
                "id": blogid,
                "author": current_user.name,
                "access_policy": {
                    "view": list(can_view),
                    "edit": list(can_edit)
                }
            }
            blogs.commit()
        return redirect(url_for("blog.edit", id=blogid))
    else:
        return render_template('blog.html', blogs=blogs)

@blog.route('/edit')
def edit():
    blogid = request.args.get('id')
    if blogid == None:
        return redirect(url_for('blog.index'))
    
    user_can = auth.rights(current_user, blogs[blogid]["access_policy"])
    
    if blogid in blogs and user_can["edit"]:
        if request.args.get("action") == "view":
            blogs[blogid]["text"] = request.args.get("text")
            blogs.commit()
            return redirect(url_for("blog.view", id=blogid))
        elif request.args.get("action") == "save":
            blogs[blogid]["text"] = request.args.get("text")
            blogs.commit()
            return redirect(url_for("blog.edit", id=blogid))
        else:
            return render_template(
                'edit_blog.html',
                 blog=blogs[blogid])
    else:
        return redirect(url_for("blog.index"))

@blog.route('/view', methods=['GET'])
def view():
    blogid = request.args.get("id")

    if blogid in blogs:
        blogg = blogs[blogid]
        print("user:",current_user)
        user_can = auth.rights(current_user, blogg["access_policy"])
        if user_can["view"]:
            content = markdown(blogs[blogid]["text"],
                extensions=["tables"])
            edit_button = """<br>
                <form action="/blog/edit">
                    <input type="hidden" name="id" value={}>
                    <input type="submit" value="Edit" />
                </form>""".format(blogid)
            head = """
                <head>
                    <link rel="stylesheet" type="text/css" href="/css/main.css">
                    <title>Blog {}</title>
                </head>
                <body>
            """.format(blogid)
            tail = "</body>"
            if user_can["edit"]:
                return head + content + edit_button + tail
            else:
                return head + content + tail
        else:
            return redirect(url_for('blog.index'))
    else:
        return redirect(url_for('blog.index'))
