from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, note
from datetime import date

dateFormat = "%m/%d/%Y %I:%M %p"


@app.route("/notes")
def notes():
    if "user_id" not in session:
        return redirect("/")
    user_id = session["user_id"]
    return render_template(
        "notes/notes.html", all_notes=note.Note.getAll({"user_id": user_id})
    )


@app.route("/notes/create")
def createNote():
    if "user_id" not in session:
        return redirect("/")
    return render_template(
        "notes/noteCreate.html",
        current_user=user.User.getById({"id": session["user_id"]}),
    )


@app.route("/notes/add", methods=["POST"])
def addNote():
    if "user_id" not in session:
        return redirect("/")
    if note.Note.validate_create(request.form):
        data = {
            "title": request.form["title"],
            "content": request.form["content"],
            "user_id": session["user_id"],
        }
        note.Note.save(data)
        return redirect("/notes")
    return redirect("/notes/create")


@app.route("/notes/edit/<int:note_id>")
def editNote(note_id):
    if "user_id" not in session:
        return redirect("/")
    session["note_id"] = note_id
    return render_template(
        "notes/noteUpdate.html",
        current_user=user.User.getById({"id": session["user_id"]}),
        current_note=note.Note.getNoteById({"id": note_id}),
    )


@app.route("/notes/update", methods=["POST"])
def updateNote():
    if "user_id" not in session:
        return redirect("/")
    if note.Note.validate_create(request.form):
        data = {
            "title": request.form["title"],
            "content": request.form["content"],
            "user_id": session["user_id"],
            "note_id": session["note_id"],
        }
        note.Note.update(data)
        return redirect("/notes")
    return redirect(f"/notes/edit/{session['note_id']}")


@app.route("/notes/view/<int:note_id>")
def viewNote(note_id):
    if "user_id" not in session:
        return redirect("/")
    else:
        if note.Note.getNoteById({"id": note_id}) is None:
            return redirect("/notes")
        else:
            note = note.Note.getNoteById({"id": note_id})
            render_template("notes/noteView.html", note=note)


@app.route("/notes/delete/<int:note_id>")
def destroyNote(note_id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": note_id}
    note.Note.destroy(data)
    return redirect("/notes")
