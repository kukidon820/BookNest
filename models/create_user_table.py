from peewee import CharField, IntegerField
from .base_model import BaseModel


class User(BaseModel):
    """
    Класс для создания таблицы user в бд
    """
    id = IntegerField(primary_key=True)
    login = CharField(max_length=20, unique=True, null=False)
    first_name = CharField(max_length=20, null=False)
    last_name = CharField(max_length=30, null=False)
    password = CharField(max_length=20, null=False)


