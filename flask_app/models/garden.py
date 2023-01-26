from flask_app.config.mysqlconnection import connectToMySQL
db = "garden_calendar"
from flask import flash
from flask_app.models import user, task, calendar
from datetime import datetime
dateFormat = '%Y-%m-%d'

class Garden:
    def __init__(self,data):
        self.id = data['id']  # need UUID hex to create hashed id
        self.garden_name = data['garden_name']
        self.location = data['location']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['garden_name']) < 1:
            flash('Please enter a name for your garden!', 'regError')
            is_valid = False
        elif len(request['garden_name']) < 3:
            flash('Garden name must be longer than two characters', 'regError')
            is_valid = False
        if len(request['location']) < 1:
            flash('Please enter the location of your garden', 'regError')
            is_valid = False
        elif len(request['location']) < 3:
            flash('Garden location must be longer than two characters', 'regError')
            is_valid = False
        if len(request['description']) < 1:
            flash('Please enter a description of your garden', 'regError')
            is_valid = False
        elif len(request['description']) < 20:
            flash('Please describe your garden, i.e purpose, what you grow, etc.', 'regError')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO gardens (id, garden_name, location, description, user_id) VALUES (%(id)s, %(garden_name)s, %(location)s, %(description)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE gardens SET garden_name = %(garden_name)s, location = %(location)s, description = %(description)s, updated_at = NOW() WHERE user_id = %(user_id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def getGarden(cls, data):
        query = """
            SELECT gardens.id AS id, garden_name, location, description, gardenss.created_at, gardens.updated_at, user_id
            FROM users
            LEFT JOIN gardens on gardens.user_id = users.id
            WHERE users.id = %(id)s; 
            """
        results = connectToMySQL(db).query_db(query, data)
        one_user = cls(results[0])
        one_user.results = results[0]['id']
        return one_user
    
