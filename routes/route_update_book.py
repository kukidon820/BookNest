from flask import render_template, Blueprint, request, flash, session, redirect, url_for
from models.create_book_table import Book
from models.create_author_table import Author

update_book_site_bp = Blueprint('update_book', __name__)

@update_book_site_bp.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    print("Переход на update_book.html")
    author_id = None
    # Попробуем загрузить книгу по `book_id`
    try:
        book = Book.get_by_id(book_id)
    except Book.DoesNotExist:
        flash("Книга не найдена.")
        return redirect(url_for('home'))

    # Обработка POST-запроса для обновления данных книги
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            flash("Вам необходимо войти в систему, чтобы изменить книгу.")
            return redirect(url_for('sing_in.route_sing_in'))

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        title = request.form.get('title')
        book_text = request.form.get('book_text')

        # Обработка автора
        author_id = None
        if first_name and last_name:
            try:
                author = Author.get_or_none(
                    first_name=first_name,
                    last_name=last_name
                )
                if author:
                    # Если автор существует, получаем его id
                    author_id = author.id
                    flash(f"Автор уже существует: {first_name} {last_name}")
                else:
                    # Если автор не существует, создаем нового автора
                    author = Author.create(
                        first_name=first_name,
                        last_name=last_name
                    )
                    author_id = author.id
                    flash(f"Автор успешно добавлен: {first_name} {last_name}")
            except Exception as e:
                print(f"Ошибка при обработке автора: {e}")
                flash("Произошла ошибка при обработке автора.")
                return render_template("update_book.html", book=book)

        # Обновляем данные книги только если поля заполнены
        try:
            if title:
                book.book_name = title
            if book_text:
                book.text = book_text
            Book.update(book_name=title, book_text=book_text, author_id=author_id).where(Book.id == book.id).execute()
            print(title, book_text, book_id, book)
            print(f"Заголовок: {book.book_name}, Текст: {book.text}")  # Проверка значений перед сохранением

            flash("Книга успешно изменена!")
            print("Книга успешно изменена!")
        except Exception as e:
            print(f"Ошибка при изменении книги: {e}")
            flash("Произошла ошибка при изменении книги.")

    # Возвращаем данные для отображения на странице
    return render_template("update_book.html", book=book)

