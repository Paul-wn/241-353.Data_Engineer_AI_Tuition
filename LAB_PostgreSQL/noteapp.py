import flask

import models
import forms


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"

models.init_app(app)


@app.route("/")
def index():
    db = models.db
    notes = db.session.execute(
        db.select(models.Note).order_by(models.Note.title)
    ).scalars()
    return flask.render_template(
        "index.html",
        notes=notes,
    )


@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = forms.NoteForm()
    if not form.validate_on_submit():
        print("error", form.errors)
        return flask.render_template(
            "notes-create.html",
            form=form,
        )
    
    # Create new note and manually set fields
    note = models.Note()
    note.title = form.title.data
    note.description = form.description.data
    note.tags = []

    db = models.db
    for tag_name in form.tags.data:
        tag = (
            db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
            .scalars()
            .first()
        )

        if not tag:
            tag = models.Tag(name=tag_name)
            db.session.add(tag)

        note.tags.append(tag)

    db.session.add(note)
    db.session.commit()

    return flask.redirect(flask.url_for("index"))


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def notes_edit(note_id):
    db = models.db
    note = db.session.execute(
        db.select(models.Note).where(models.Note.id == note_id)
    ).scalars().first()
    
    if not note:
        flask.abort(404)
    
    form = forms.NoteForm(obj=note)
    # Pre-populate tags field with existing tag names
    if flask.request.method == "GET":
        form.tags.data = [tag.name for tag in note.tags]
    
    if not form.validate_on_submit():
        return flask.render_template(
            "note-edit.html",
            form=form,
            note=note,
        )
    
    # Manually update note fields instead of using populate_obj
    note.title = form.title.data
    note.description = form.description.data
    
    # Clear existing tags and add new ones
    note.tags.clear()
    for tag_name in form.tags.data:
        tag = (
            db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
            .scalars()
            .first()
        )
        
        if not tag:
            tag = models.Tag(name=tag_name)
            db.session.add(tag)
        
        note.tags.append(tag)
    
    db.session.commit()
    return flask.redirect(flask.url_for("index"))


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def notes_delete(note_id):
    db = models.db
    note = db.session.execute(
        db.select(models.Note).where(models.Note.id == note_id)
    ).scalars().first()
    
    if not note:
        flask.abort(404)
    
    db.session.delete(note)
    db.session.commit()
    return flask.redirect(flask.url_for("index"))


@app.route("/tags/<tag_name>")
def tags_view(tag_name):
    db = models.db
    tag = (
        db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
        .scalars()
        .first()
    )
    
    if not tag:
        flask.abort(404)
    
    notes = db.session.execute(
        db.select(models.Note).where(models.Note.tags.any(id=tag.id))
    ).scalars()

    return flask.render_template(
        "tags-view.html",
        tag_name=tag_name,
        tag=tag,
        notes=notes,
    )


@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def tags_edit(tag_id):
    db = models.db
    tag = db.session.execute(
        db.select(models.Tag).where(models.Tag.id == tag_id)
    ).scalars().first()
    
    if not tag:
        flask.abort(404)
    
    form = forms.TagForm(obj=tag)
    
    if not form.validate_on_submit():
        return flask.render_template(
            "tags-edit.html",
            form=form,
            tag=tag,
        )
    
    # Manually update the tag name instead of using populate_obj
    tag.name = form.name.data
    db.session.commit()
    return flask.redirect(flask.url_for("tags_view", tag_name=tag.name))


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tags_delete(tag_id):
    db = models.db
    tag = db.session.execute(
        db.select(models.Tag).where(models.Tag.id == tag_id)
    ).scalars().first()
    
    if not tag:
        flask.abort(404)
    
    # Remove the tag from all notes that use it
    notes_with_tag = db.session.execute(
        db.select(models.Note).where(models.Note.tags.any(id=tag.id))
    ).scalars().all()
    
    for note in notes_with_tag:
        note.tags.remove(tag)
    
    # Now we can safely delete the tag
    db.session.delete(tag)
    db.session.commit()
    return flask.redirect(flask.url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
