from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, garden, container
from datetime import datetime
import uuid
dateFormat = "%m/%d/%Y %I:%M %p"

@app.route("/gardens")
def displayGarden():
    if "user_id" not in session:
        return redirect("/")
    return render_template("garden.html", current_user = user.User.getById({'id' : session['user_id']}), garden = garden.Garden.getGarden({'id' : session['user_id']}), all_containers = container.Container.getAll())

@app.route("/gardens/create", methods=['POST'])
def createGarden():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('gardenCreate.html', current_user = user.User.getById({'id' : session['user_id']}))

@app.route('/gardens/add', methods=['POST'])
def addGarden():
    if 'user_id' not in session:
        return redirect("/")
    if garden.Garden.validate_create(request.form):
        data = {
            'id' : uuid.uuid4(),
            'garden_name': request.form['garden_name'],
            'location': request.form['location'],
            'description': request.form['description'],
            'user_id': session['user_id']
        }
        garden.Garden.save(data)
        return redirect('/gardens')
    return redirect('/gardens/create')

@app.route('/gardens/edit/<int:user_id>')
def editGarden(user_id):
    if 'user_id' not in session:
        return redirect("/")
    return render_template('gardenUpdate.html', current_user = user.User.getById({'id' : session['user_id']}),  garden = garden.Garden.getGarden({'id' : session['user_id']}))

@app.route('/gardens/update', methods=['POST'])
def updateGarden():
    if 'user_id' not in session:
        return redirect("/")
    if garden.Garden.validate_create(request.form):
        data = {
            'garden_name' : request.form['garden_name'],
            'location' : request.form['location'],
            'description' : request.form['description'],
            'user_id' : session['user_id']
        }
        garden.Garden.update(data)
        return redirect('/gardens')
    return redirect(f"/gardens/edit/{session['user_id']}")


@app.route('/gardens/container')
def addContainer():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('containerCreate.html', current_user = user.User.getById({'id' : session['user_id']}))

@app.route('/gardens/container/add', methods=['POST'])
def saveContainer():
    if 'user_id' not in session:
        return redirect('/')
    if container.Container.validate_create(request.form):
        data = {
            'name' : request.form['name'],
            'count' : request.form['count'],
            'garden_id' : request.form['garden_id'] # Need to add a hidden input for garden_id on the form
        }
        container.Container.save(data)
        return redirect('/gardens')
    return redirect('/gardens/container')
    
