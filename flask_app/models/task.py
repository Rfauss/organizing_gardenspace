from flask_app.config.mysqlconnection import connectToMySQL

db = "garden_calendar"
from flask import flash, session
from flask_app.models import user, garden
from datetime import datetime

dateFormat = "%Y-%m-%d"
today = datetime.today()


class Task:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.status = data["status"]
        self.date = data["date"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.garden_id = data["garden_id"]
        self.calendar_id = data["calendar_id"]

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request["title"]) < 1:
            flash("Please enter a title for the task", "taskError")
            is_valid = False
        elif len(request["title"]) < 5:
            flash("Please provide a more detailed title", "taskError")
            is_valid = False
        if len(request["description"]) < 1:
            flash("Please describe the task", "taskError")
            is_valid = False
        elif len(request["description"]) < 20:
            flash("Please give more detail so it can be done right!", "taskError")
            is_valid = False
        if len(request["date"]) < 1:
            flash("Please enter a due date for this task", "taskError")
            is_valid = False
        elif datetime.strptime(request["due_date"], dateFormat) < today:
            flash("Date cannot be in the past or same day", "taskError")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO tasks (title, description, date, garden_id, calendar_id) VALUES (%(title)s, %(description)s, %(date)s, %(garden_id)s, %(calendar_id)s);"
        return connectToMySQL(db).query_db(query, data)

        # Form for Save method will need to pass hidden input for garden_id and calendar_id

    @classmethod
    def update(cls, data):
        query = "UPDATE tasks SET title = %(title)s, description = %(description)s, date = %(date)s, status = %(status)s, updated_at = NOW(), garden_id = %(garden_id)s WHERE id = %(task_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM tasks WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def getTaskByGarden(cls, data):
        query = """
            SELECT tasks.id, title, tasks.description, date, status, tasks.created_at, tasks.updated_at, tasks.garden_id, tasks.calendar_id,
            FROM gardens
            LEFT JOIN tasks
            ON gardens.id = tasks.garden_id
            WHERE tasks.id = %(task_id)s;
            """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        view_one = cls(results[0])
        return view_one

    @classmethod
    def getAll(cls):
        query = """
            SELECT tasks.id, title, tasks.description, date, status, tasks.created_at, tasks.updated_at,
            gardens.id as garden_id, garden_name, location, gardens.description, gardens.created_at as uca, gardens.updated_at as uua,
            FROM tasks
            JOIN gardens on gardens.id = tasks.garden_id;
            """
        tasks_from_db = connectToMySQL(db).query_db(query)
        tasks = []
        for task in tasks_from_db:
            task_object = cls(task)
            task_object.garden = garden.Garden(
                {
                    "id": task["garden_id"],
                    "garden_name": task["garden_name"],
                    "location": task["location"],
                    "description": task["description"],
                    "created_at": task["uca"],
                    "updated_at": task["uua"],
                }
            )
            tasks.append(task_object)
            print(tasks[0])
        return tasks

    @classmethod
    def inProgress(cls, data):
        query = "UPDATE tasks SET status = 'In Progress' WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def markComplete(cls, data):
        query = "UPDATE tasks SET status = 'Completed' WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
