from flask import render_template, Blueprint, session
from peewee import prefetch
from models.create_book_table import Book
from models.create_author_table import Author

home_site_bp = Blueprint("home", __name__)


@home_site_bp.route("/", methods=["GET"])
def route_home():
    """
        Отображает главную страницу с книгами, принадлежащими текущему пользователю.

        Функция выполняет следующие действия:
        1. Загружает книги, связанные с текущим пользователем, из базы данных с использованием метода `prefetch`,
           чтобы минимизировать количество запросов к базе данных.
        2. Отображает главную страницу (`home.html`) с загруженными книгами.

        Возвращает:
            - HTML-шаблон главной страницы (`home.html`) с контекстом, содержащим список книг.

        Пример запроса:
            GET /
    """

    print("переход на home.html")

    # Загрузка книг и соответствующих авторов
    books = prefetch(Book.select().where(Book.user_id == session.get("user_id")), Author)

    return render_template("home.html", books=books)
