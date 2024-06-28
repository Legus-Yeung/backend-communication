from flask import Flask, request, jsonify
from flask_cors import CORS
from peewee import *
from playhouse.shortcuts import model_to_dict
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv('DB_PASSWORD')
database = os.getenv('DB')
endpoint = os.getenv('DB_URL')

app = Flask(__name__)
CORS(app)

db = MySQLDatabase(database, user='admin', password=password, host=endpoint)

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    first_name = CharField()
    last_name = CharField()

    def to_json(self):
        return model_to_dict(self)

@app.before_request
def initialize_database():
    if not hasattr(initialize_database, 'initialized'):
        initialize_database.initialized = True
        db.connect()
        db.create_tables([Users], safe=True)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    user = Users.create(first_name=data['first_name'], last_name=data['last_name'])
    return jsonify(user.to_json()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users_query = Users.select()
    users = [user.to_json() for user in users_query]
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(debug=True)
