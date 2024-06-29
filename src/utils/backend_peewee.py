from peewee import *
from playhouse.shortcuts import model_to_dict
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv('DB_PASSWORD')
database = os.getenv('DB')
endpoint = os.getenv('DB_URL')

db = MySQLDatabase(database, user='admin', password=password, host=endpoint)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    first_name = CharField()
    last_name = CharField()

    def to_json(self):
        return model_to_dict(self)

db.connect()
db.create_tables([User], safe=True)