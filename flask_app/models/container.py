from flask_app.config.mysqlconnection import connectToMySQL
db = "garden_calendar"
from flask import flash, session
from flask_app.models import user, garden
from datetime import datetime
dateFormat = '%Y-%m-%d'
today = datetime.today()

class Container:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.count = data['count']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.garden_id = data['garden_id']

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['name']) < 1:
            flash('Please enter a name for the plant', 'containerError')
            is_valid = False
        elif len(request['name']) < 3:
            flash('Name must be at least 3 characters', 'containerError')
            is_valid = False
        if len(request['count']) < 1:
            flash('Please enter how many plants are here', 'containerError')
            is_valid = False
        elif request['count'] < 1:
            flash('Must have at least one plant in the container', 'taskError')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO containers (name, count, garden_id) VALUES (%(name)s, %(count)s, %(garden_id)s);"
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    def update(cls,data):
        query = "UPDATE containers SET name = %(name)s, count = %(count)s, updated_at = NOW(), garden_id = %(garden_id)s WHERE id = %(container_id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM containers WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def getAll(cls):
        query = """
            SELECT containers.id, containers.name, count, containers.created_at, containers.updated_at,
            gardens.id as garden_id, garden_name, location, gardens.description, gardens.created_at as uca, gardens.updated_at as uua,
            FROM containers
            JOIN gardens on gardens.id = containers.garden_id;
            """
        containers_from_db = connectToMySQL(db).query_db(query)
        containers = []
        for container in containers_from_db:
            container_object = cls(container)
            container_object.garden = garden.Garden( 
                {
                    "id": container["garden_id"],
                    "garden_name": container["garden_name"],
                    "location": container["location"],
                    "description": container["description"],
                    "created_at": container["uca"],
                    "updated_at": container["uua"]
                }
            )
            containers.append(container_object)
        return containers
