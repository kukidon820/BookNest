from peewee import CharField, IntegerField
from .base_model import BaseModel

class Author(BaseModel):
    """
    Класс для создания таблицы Author в бд
    """
    id = IntegerField(primary_key=True)
    first_name = CharField(max_length=20, null=False)
    last_name = CharField(max_length=30, null=False)
