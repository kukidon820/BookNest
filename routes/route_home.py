from flask import render_template, Blueprint, session
from peewee import prefetch
from models.create_book_table import Book
from models.create_author_table import Author

home_site_bp = Blueprint("home", __name__)

@home_site_bp.route("/", methods=["GET"])
def route_home():
    print("переход на home.html")

    # Загрузка книг и соответствующих авторов
    books = prefetch(Book.select().where(Book.user_id == session.get("user_id")), Author)

    return render_template("home.html", books=books)
