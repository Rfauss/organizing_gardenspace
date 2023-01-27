from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, note
from datetime import datetime

dateFormat = "%m/%d/%Y %I:%M %p"

@app.route("/notes")
def notes():
    if "user_id" not in session:
        return redirect('/')
    return render_template("notes.html", all_notes = note.Note.getAll())

@app.route("/notes/create")
def createNote():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('noteCreate.html', current_user = user.User.getById({'id' : session['user_id']}))

@app.route("/notes/add")
def addNote():
    if 'user_id' not in session:
        return redirect('/')
    if note.Note.validate_create(request.form):
        data = {
            'title': request.form['title'],
            'content': request.form['content'],
            'date': request.form['date'],
            'due_date' : request.form['due_date'],
            'user_id' : request.form['user_id']
        }
        note.Note.save(data)
        return redirect('/notes')
    return redirect('/notes/create')

@app.route("/notes/edit/<int:note_id>")
def editNote(note_id):
    if 'user_id' not in session:
        return redirect('/')
    session['note_id'] = note_id
    return render_template('noteUpdate.html', current_user = user.User.getById({'id': session['user_id']}), note = note.Note.getNoteByUser({'note_id' : note_id}))

@app.route("/notes/update", methods=['POST'])
def updateNote():
    if 'user_id' not in session:
        return redirect("/")
    if note.Note.validate_create(request.form):
        data = {
            'title': request.form['title'],
            'content': request.form['content'],
            'date': request.form['date'],
            'due_date' : request.form['due_date'],
            'user_id' : request.form['user_id']
        }
        note.Note.update(data)
        return redirect("/notes")
    return redirect(f"/notes/edit/{session['note_id']}")

@app.route("/notes/view")
def viewNote():
    pass
# I don't know how you want to render the view - you had talked about doing a modal. Can update as/if necessary

@app.route("/notes/delete/<int:note_id>")
def destroyNote(note_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : note_id
    }
    note.Note.destroy(data)
    return redirect('notes')