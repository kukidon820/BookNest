from peewee import CharField, IntegerField, DateTimeField, ForeignKeyField, TextField
from .base_model import BaseModel
from .create_user_table import User
from .create_author_table import Author

class Book(BaseModel):
    """
    Класс для создания таблицы Book
    """
    id = IntegerField(primary_key=True)
    user_id = ForeignKeyField(User, backref='post')
    book_name = CharField(max_length=100, null=False)
    book_text_id = CharField(max_length=24, null=False)
    author_id = ForeignKeyField(Author, backref='post')
    time_added = DateTimeField()

