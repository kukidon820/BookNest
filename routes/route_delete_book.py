from flask import Blueprint, redirect, url_for, flash, session
from models.create_book_table import Book

delete_book_bp = Blueprint('delete_book', __name__)


@delete_book_bp.route("/delete_book/<int:book_id>", methods=["GET", "POST"])
def delete_book(book_id):
    """
        Удаляет книгу из базы данных по указанному идентификатору.

        Функция выполняет следующие действия:
        1. Проверяет наличие user_id в сессии. Если user_id отсутствует, пользователь перенаправляется на страницу входа с сообщением об ошибке.
        2. Пытается найти книгу по переданному идентификатору book_id.
        3. Проверяет, принадлежит ли книга пользователю, осуществляющему запрос. Если книга не принадлежит пользователю, отображается сообщение об ошибке.
        4. Если книга найдена и принадлежит пользователю, происходит удаление книги из базы данных, и отображается сообщение об успешном удалении.
        5. Обрабатывает исключения, если книга не найдена или если происходит ошибка при удалении.

        Возвращает:
            - Перенаправление на главную страницу после удаления книги или в случае ошибки.

        Пример запроса (POST):
            POST /delete_book/1
    """

    print("Переход на delete_book.html")
    user_id = session.get('user_id')

    if not user_id:
        flash("Вам необходимо войти в систему, чтобы удалить книгу.")
        return redirect(url_for('sing_in.route_sing_in'))

    try:
        # Попробуем найти книгу по ID и проверить, принадлежит ли она пользователю
        book = Book.get_by_id(book_id)

        # Предположим, что в модели Book есть поле user_id, связывающее книгу с пользователем
        if str(book.user_id) != str(user_id):
            flash("У вас нет прав для удаления этой книги.")
            print(f"У вас нет прав для удаления этой книги.{book.user_id} {user_id}")
            return redirect(url_for('home.route_home'))

        # Удаление книги из базы данных
        book.delete_instance()
        flash("Книга успешно удалена!")
        print("Книга успешно удалена!")
    except Book.DoesNotExist:
        flash("Книга не найдена.")
    except Exception as e:
        print(f"Ошибка при удалении книги: {e}")
        flash("Произошла ошибка при удалении книги.")

    return redirect(url_for('home.route_home'))  # Перенаправляем на главную страницу после удаления
