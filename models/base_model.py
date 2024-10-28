from peewee import Model
from .add_all_tables_in_database import db
class BaseModel(Model):
    class Meta:
        database = db