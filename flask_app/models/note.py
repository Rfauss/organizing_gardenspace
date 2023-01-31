from flask_app.config.mysqlconnection import connectToMySQL

db = "garden_calendar"
from flask import flash, session
from flask_app.models import user, garden
from datetime import datetime

dateFormat = "%Y-%m-%d"
today = datetime.today()


class Note:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.content = data["content"]
        self.date = data["date"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    # Pass user_id via session

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request["title"]) < 1:
            flash("Please enter a title for your note", "noteError")
            is_valid = False
        elif len(request["title"]) < 4:
            flash("Please provide a more detailed title", "noteError")
            is_valid = False
        if len(request["content"]) < 1:
            flash("Please leave a description for your note", "noteError")
            is_valid = False
        elif len(request["content"]) < 20:
            flash("Please give more detail!", "noteError")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO notes (title, content, date, user_id) VALUES (%(title)s, %(content)s, NOW(), %(user_id)s)"
        return connectToMySQL(db).query_db(query, data)

        # Pass user_id via session

    @classmethod
    def update(cls, data):
        query = "UPDATE notes SET title = %(title)s, content = %(content)s, date = NOW(), updated_at = NOW(), user_id = %(user_id)s WHERE id = %(note_id)s;"
        return connectToMySQL(db).query_db(query, data)

        # Pass user_id via session

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM notes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def getNoteByUser(cls, data):
        query = """
            SELECT notes.id, title, notes.content, date, notes.created_at, notes.updated_at, notes.user_id
            FROM users
            LEFT JOIN notes
            ON users.id = notes.user_id
            WHERE notes.id = %(note_id)s;
            """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        view_one = cls(results[0])
        return view_one

    @classmethod
    def getAll(cls, data):
        query = "SELECT * FROM notes WHERE user_id = %(user_id)s;"
        notes_from_db = connectToMySQL(db).query_db(query, data)
        print(notes_from_db)
        return notes_from_db

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM notes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def getNoteById(cls, data):
        query = "SELECT * FROM notes WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        return results
