from flask_app.config.mysqlconnection import connectToMySQL
db = "garden_calendar"
from flask import flash
from datetime import datetime
dateFormat = '%Y-%m-%d'
from flask_app.models import user, garden, task, calendar
import re
PW_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")

class Calendar:
    def __init__(self,data):
        self.id = data['id']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.garden_id = data['garden_id']

    
    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM calendars WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod 
    def getAllTasksByCalID(cls):
        query = """
            SELECT tasks.id, title, tasks.description, status, date, tasks.created_at, tasks.updated_at, tasks.garden_id, tasks.calendar_id,
            gardens.id, location, gardens.description, gardens.created_at as gca, gardens.updated_at as gua, gardens.user_id
            from tasks
            LEFT JOIN calendars on calendars.id = tasks.calendar_id
            LEFT JOIN gardens on gardens.id = tasks.garden_id
            """
        tasks_from_db = connectToMySQL(db).query_db(query)
        tasks = []
        for task in tasks_from_db:
            task_object = cls(task)
            task_object.calendar = calendar.Calendar(
                {
                    "id": task["calendar_id"],
                    "date": task["date"],
                    "created_at": task["created_at"],
                    "updated_at": task["updated_at"],
                    "user_id" : task["user_id"],
                    "garden_id" : task["garden_id"]
                }
            )
            tasks.append(task_object)
        return tasks
