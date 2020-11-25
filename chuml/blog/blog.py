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
    if blogid and blogid.isalnum() and current_user.is_authenticated and not blogid in blogs:
        blogs[blogid] = {
            "text": "",
            "id": blogid,
            "author": current_user.name,
            "access_policy": {
                "view": ['@'+current_user.name],
                "edit": ['@'+current_user.name]
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
    
    user_can = auth.rights(blogs[blogid]["access_policy"])
    
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
        user_can = auth.rights(blogg["access_policy"])
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
            flash("Permission denied.")
            return redirect(url_for('blog.index'))
    else:
        return redirect(url_for('blog.index'))

@blog.route('/append')
def append():
    blogid = request.args.get('id')

    if not blogid in blogs:
        flash("Blog " + blogid + " does not exist.")
        return redirect(url_for('blog.index'))
    
    user_can = auth.rights(blogs[blogid]["access_policy"])
    if not user_can["edit"]:
        flash("Permission denied.")
        return redirect(url_for('blog.index'))

    line = request.args.get('line')
    if line == None:
        flash("`line` arg required.")
        return redirect(url_for('blog.index'))
    
    blogs[blogid]["text"] += "  \n" + line
    blogs.commit()

    return redirect(url_for("blog.view", id=blogid))

