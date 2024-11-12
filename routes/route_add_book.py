from flask import render_template, Blueprint, request, flash, session, redirect, url_for
from datetime import datetime
from models.create_book_table import Book
from models.create_author_table import Author

add_book_site_bp = Blueprint('add_book', __name__)


@add_book_site_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
        Обрабатывает добавление новой книги через веб-форму.

        При получении POST-запроса функция выполняет следующие действия:
        1. Проверяет наличие user_id в сессии. Если user_id отсутствует, пользователь перенаправляется на страницу входа с сообщением об ошибке.
        2. Извлекает имя и фамилию автора из формы.
        3. Пытается найти или создать автора в базе данных. Если автор был создан, отображается сообщение об успехе; если автор уже существует, отображается соответствующее уведомление.
        4. Создает и сохраняет новую книгу, связанную с пользователем. Время добавления книги фиксируется на текущий момент.

        Возвращает:
            - Если метод запроса GET, возвращает HTML-шаблон "add_book.html".
            - Если метод запроса POST и добавление книги прошло успешно, отображается уведомление об успешном добавлении книги.
            - Если возникает ошибка на любом этапе (при обработке автора или добавлении книги), пользователю показывается соответствующее сообщение об ошибке.

        Пример запроса (POST):
            POST /add_book
            {
                "first_name": "Лев",
                "last_name": "Толстой",
                "title": "Война и мир",
                "book_text": "https://example.com/book_text"
            }
        """

    if request.method == 'POST':
        # Проверка на наличие user_id в сессии
        user_id = session.get('user_id')
        if not user_id:
            flash("Вам необходимо войти в систему, чтобы добавить книгу.")
            return redirect(url_for('sing_in.route_sing_in'))

        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Пытаемся найти или создать автора
        try:
            author, created = Author.get_or_create(
                first_name=first_name,
                last_name=last_name
            )
            author_id = author.id

            if created:
                flash(f"Автор {first_name} {last_name} успешно добавлен!")
            else:
                flash(f"Автор {first_name} {last_name} уже существует.")

        except Exception as e:
            print(f"Ошибка при обработке автора: {e}")
            flash("Произошла ошибка при обработке автора.")
            return render_template("add_book.html")

        # Создаем и сохраняем книгу
        try:
            new_book = Book(
                user_id=user_id,
                book_name=request.form['title'],
                book_text=request.form['book_text'],
                author_id=author_id,
                time_added=datetime.now()
            )
            new_book.save()
            flash("Книга успешно добавлена!")
        except Exception as e:
            print(f"Ошибка при добавлении книги: {e}")
            flash("Произошла ошибка при добавлении книги.")

    return render_template("add_book.html")
