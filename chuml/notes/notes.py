# notes.py

from flask import Flask, request, redirect, \
				  url_for, render_template, \
				  Blueprint, flash

from markdown import markdown

from flask_login import current_user, login_required

from chuml.utils import db
from chuml.auth import auth
from chuml.auth import access
from chuml.models import Note, Label

notes = Blueprint('notes', __name__,
    template_folder='templates',
    url_prefix='/note')

@notes.route('/')
def index():
    notes = [ note for note in db.query(Note).all()
              if access.access(note) > access.NOTHING ]

    return render_template("notes.html",notes=notes)

@notes.route("/create")
@login_required
def create():
    note = Note(
        text = request.args.get("text"),
        name = request.args.get("name")
    )
    db.add(note)
    db.commit()
    return redirect(url_for("notes.edit",id=note.id))


@notes.route('/<id>/edit')
def edit(id=0):
    note = db.query(Note).get(id)
    if not note:
        flash("Note {} not found.".format(id))
        return redirect(url_for('notes.index'))
    
    if access.access(note) < access.EDIT:
        return access.forbidden_page()
    
    if request.args.get("action") == "view":
        note.text = request.args.get("text")
        note.name = request.args.get("name")
        db.commit()
        flash("{} saved.".format(note.name))
        return redirect(url_for("notes.view", id=id))
    elif request.args.get("action") == "save":
        note.text = request.args.get("text")
        note.name = request.args.get("name")
        db.commit()
        flash("{} saved.".format(note.name))
        return redirect(url_for("notes.edit", id=id))
    elif request.args.get("action") == "delete":
        note.labels.clear()
        db.delete(note)
        db.commit()
        flash("{} deleted.".format(note.name))
        return redirect(url_for('notes.index'))
    else:
        return render_template(
            'edit_note.html',
             note=note,
            )

@notes.route('/<id>/view', methods=['GET'])
def view(id=0):
    note = db.query(Note).get(id)
    if not note:
        flash("Note {} not found.".format(id))
        return redirect(url_for('notes.index'))
    
    if access.access(note) < access.VIEW:
        return access.forbidden_page()

    rendered = markdown(note.text, extensions=["tables"])
    return render_template(
            'view_note.html',
             note=note,
             rendered=rendered,
             user_can_edit=access.access(note) >= access.EDIT)

@notes.route('/<id>/append')
def append(id=0):
    note = db.query(Note).get(id)
    if not note:
        flash("Note {} not found.".format(id))
        return redirect(url_for('notes.index'))
    
    if access.access(note) < access.EDIT:
        return access.forbidden_page()

    line = request.args.get('line')
    if line == None:
        flash("`line` arg required.")
        return redirect(url_for('notes.index'))
    
    note.text += "  \n" + line
    db.commit()
    flash("<i>{}</i> appended to {}.".format(line,note.name))

    return redirect(url_for("notes.view", id=id))

