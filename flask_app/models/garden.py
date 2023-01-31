from flask_app.config.mysqlconnection import connectToMySQL

db = "garden_calendar"
from flask import flash
from flask_app.models import user, task
from datetime import datetime

dateFormat = "%Y-%m-%d"


class Garden:
    def __init__(self, data):
        self.id = data["id"]  # need UUID hex to create hashed id
        self.garden_name = data["garden_name"]
        self.location = data["location"]
        self.rows = data["rows"]
        self.columns = data["columns"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = None

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request["garden_name"]) < 1:
            flash("Please enter a name for your garden!", "regError")
            is_valid = False
        elif len(request["garden_name"]) < 3:
            flash("Garden name must be longer than two characters", "regError")
            is_valid = False
        if len(request["location"]) < 1:
            flash("Please enter the location of your garden", "regError")
            is_valid = False
        elif len(request["location"]) < 3:
            flash("Garden location must be longer than two characters", "regError")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_plants(request):
        is_valid = True
        if len(request["plant_name"]) < 1:
            flash("Please enter a name for your plant!", "regError")
            is_valid = False
        elif len(request["plant_name"]) < 3:
            flash("Plant name must be longer than two characters", "regError")
            is_valid = False
        if int(request["plant_count"]) < 1:
            flash("Must have at least one plant", "regError")
            is_valid = False
        elif int(request["plant_count"]) > 12:
            flash("Can't put that many plants that close together", "regError")
            is_valid = False
        return is_valid

    @classmethod
    def getGarden(cls, data):
        query = "SELECT * FROM gardens WHERE user_id = %(user_id)s"
        results = connectToMySQL(db).query_db(query, data)
        if results == ():
            return False
        else:
            return results

    @classmethod
    def save(cls, data):
        query = "INSERT INTO gardens (garden_name, location, gardens.rows, gardens.columns, created_at, user_id) VALUES (%(garden_name)s, %(location)s, %(rows)s, %(columns)s, NOW(), %(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        countRow = 1
        countCol = 1
        count = 0
        for row in range(data["rows"]):
            for column in range(data["columns"]):
                count += 1
                countStrCol = str(countCol)
                countStrRow = str(countRow)
                # Below string formatting is intentional, leave as is.
                name = f'"row_{countStrRow}col_{countStrCol}"'
                query = f"INSERT INTO containers (containers.name, count, created_at, garden_id) VALUES ({name}, {count}, NOW(), {results})"
                connectToMySQL(db).query_db(query, data)
                countCol += 1
            countRow += 1
            countCol = 1
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE gardens SET garden_name = %(garden_name)s, location = %(location)s, updated_at = NOW() WHERE user_id = %(user_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def getContainers(cls, data):
        query = "SELECT id,name,count FROM containers WHERE garden_id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        if results == ():
            return False
        else:
            return results

    @classmethod
    def insertIntoContainers(cls, data):
        query = "INSERT INTO plants (name,count,container_id,created_at) VALUES (%(name)s,%(count)s,%(container_id)s, NOW())"
        results = connectToMySQL(db).query_db(query, data)
        if results == ():
            return False
        else:
            return results

    @classmethod
    def updateContainer(cls, data):
        query = "UPDATE plants SET name = %(name)s, count = %(count)s, container_id = %(container_id)s, updated_at = NOW() WHERE id = %(plant_id)s"
        results = connectToMySQL(db).query_db(query, data)
        if results == ():
            return False
        else:
            return results

    @classmethod
    def getPlants(cls, data):
        query = "SELECT id,name,count,container_id FROM plants WHERE container_id = %(container_id)s"
        results = connectToMySQL(db).query_db(query, data)
        if results == ():
            return False
        else:
            return results

    @classmethod
    def deletePlants(cls, data):
        query = "DELETE FROM plants WHERE container_id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        if results == ():
            return True
        else:
            return False

    @classmethod
    def deleteAllContainers(cls, data):
        query = "DELETE FROM containers WHERE garden_id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        if results == ():
            return True
        else:
            return False

    @classmethod
    def deleteGarden(cls, data):
        query = "DELETE FROM gardens WHERE user_id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        if results == ():
            return True
        else:
            return False
