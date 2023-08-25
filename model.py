from peewee import Model, IntegerField, TextField
from database import db

class BaseModel(Model):
    class Meta:
        database = db

class Task(BaseModel):
    task_id = IntegerField(primary_key=True)
    task_title = TextField(null=True)
    task_description = TextField(null=True)
    task_state = TextField(null=True)
    user_id = IntegerField(null=True)
    
    class Meta:
        table_name = 'task'