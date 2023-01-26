from flask_app.config.mysqlconnection import connectToMySQL
db = "garden_calendar"
from flask import flash
from datetime import datetime
dateFormat = '%Y-%m-%d'
from flask_app.models import note, calendar
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")


class User:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.zip_code = data['zip_code']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.garden = None

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['name']) < 1:
            flash('Please enter your full name', 'regError')
            is_valid = False
        elif len(request['name']) < 6:
            flash('Name must be longer than 6 characters', 'regError')
            is_valid = False
        if len(request['zip_code']) < 1:
            flash('Please enter your zip code', 'regError')
            is_valid = False
        elif len(request['zip_code']) != 5:
            flash('Please enter your 5 digit zip code', 'regError')
            is_valid = False
        elif request['zip_code'].isdigit() != True:
            flash('Zip code must be 5 numerical values', 'regError')
            is_valid = False
        if len(request['email']) < 1:
            flash('Please enter an email address', 'regError')
            is_valid = False
        elif not EMAIL_REGEX.match(request['email']):
            flash('Invalid email address', 'regError')
            is_valid = False
        if User.getByEmail(request) != False:
            flash("Email is already registered", 'regError')
            is_valid = False
        if len(request['password']) < 1:
            flash('Please enter a password', 'regError')
            is_valid = False
        elif not PW_REGEX.match(request['password']):
            flash('Password must be at least 8 characters and contain at least one: Uppercase letter, lowercase letter, and number', 'regError')
            is_valid = False
        if len(request['passConf']) < 1:
            flash('Please confirm your password', 'regError')
            is_valid = False
        elif  request['password'] != request['passConf']:
            flash('Passwords do not match', 'regError')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (name, zip_code, email, password) VALUES (%(name)s, %(zip_code)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM users;"
        users_from_db = connectToMySQL(db).query_db(query)
        users = []
        for user in users_from_db:
            users.append(cls(user))
        return users

    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET name = %(name)s, zip_code = %(zip_code)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def getByEmail(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])