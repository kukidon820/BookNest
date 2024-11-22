import os
from peewee import SqliteDatabase

# Определение пути к текущей папке
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Определение полного пути к базе данных
db_path = os.path.join(BASE_DIR, 'database_library.db')

# Подключение базы данных через Peewee
db = SqliteDatabase(db_path)

def create_tables():
    from .create_user_table import User
    from .create_book_table import Book
    from .create_author_table import Author

    # Подключение к бд
    db.connect()

    # Добавление таблицы в бд
    db.create_tables([User, Book, Author], safe=True)

    # Закрытие соединения
    db.close()

