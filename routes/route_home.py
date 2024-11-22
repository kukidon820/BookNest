from flask import render_template, Blueprint, session
from peewee import prefetch
from models.create_book_table import Book
from models.create_author_table import Author
from models.functions_for_mongo import get_book_text_from_mongo

home_site_bp = Blueprint("home", __name__)

@home_site_bp.route("/", methods=["GET"])
def route_home():
    """
        Отображает главную страницу с книгами, принадлежащими текущему пользователю.

        Функция выполняет следующие действия:
        1. Загружает книги, связанные с текущим пользователем, из базы данных с использованием метода `prefetch`,
           чтобы минимизировать количество запросов к базе данных.
        2. Добавляет тексты книг из MongoDB к каждой книге.
        3. Отображает главную страницу (`home.html`) с загруженными книгами.

        Возвращает:
            - HTML-шаблон главной страницы (`home.html`) с контекстом, содержащим список книг.

        Пример запроса:
            GET /
    """

    print("Переход на home.html")

    # Загрузка книг и соответствующих авторов
    books = prefetch(Book.select().where(Book.user_id == session.get("user_id")), Author)

    # Дополнение книг текстами из MongoDB
    enriched_books = []
    for book in books:
        enriched_books.append({
            "id": book.id,
            "name": book.book_name,
            "author_id": f"{book.author_id.first_name} {book.author_id.last_name}",
            "book_text_id": book.book_text_id,
            "time_added": book.time_added,
        })

    # Передача книг с текстами в шаблон
    return render_template("home.html", books=enriched_books)
