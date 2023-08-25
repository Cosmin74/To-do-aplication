from peewee import Model, IntegerField, TextField
from database import db

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    last_name = TextField(null=True)
    first_name = TextField(null=True)
    email = TextField(null=True)
    encrypt_pass = TextField(null=True)

    class Meta:
        table_name = 'users'    