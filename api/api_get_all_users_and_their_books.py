from models.create_book_table import Book
from flask import jsonify, Blueprint
from models.create_author_table import Author
from models.create_user_table import User

api_get_all_users_and_their_books_bp = Blueprint('get_users_and_their_books', __name__)


@api_get_all_users_and_their_books_bp.route('/api/get_all_users_and_books', methods=['GET'])
def get_all_users_and_books():
    """
        Получает список всех пользователей и их книг из базы данных.

        Возвращает:
            - Если пользователи и книги найдены:
                Возвращает JSON-массив, содержащий информацию о пользователях и их книгах с статусом 200.
                Каждый объект пользователя имеет следующую структуру:
                {
                    "id": int,                   # Уникальный идентификатор пользователя
                    "first_name": str,           # Имя пользователя
                    "last_name": str,            # Фамилия пользователя
                    "books": [                   # Список книг, принадлежащих пользователю
                        {
                            "id": int,           # Уникальный идентификатор книги
                            "book_name": str,    # Название книги
                            "book_text": str,    # Текст книги (URL или текстовый контент)
                            "author": str,       # Имя и фамилия автора книги
                            "time_added": str     # Дата и время добавления книги
                        },
                        ...
                    ]
                }

            - Если пользователи или книги не найдены:
                Возвращает JSON с сообщением об отсутствии пользователей или книг и статусом 404.
                Пример: {"message": "No users or books found"}

            - В случае любой ошибки при выполнении запроса:
                Возвращает JSON с сообщением об ошибке и статусом 500.
                Пример: {"error": "Описание ошибки"}

        Пример запроса:
            GET /api/get_all_users_and_books
        """

    try:
        users_and_books = []
        for user in User.select():
            user_info = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                "books": []
            }
            user_books = Book.select().join(Author).where(Book.user_id == user.id)
            for book in user_books:
                user_info["books"].append({
                    'id': book.id,
                    'book_name': book.book_name,
                    'book_text': book.book_text,
                    'author': book.author_id.first_name + ' ' + book.author_id.last_name,
                    'time_added': book.time_added
                })
            users_and_books.append(user_info)
        return (jsonify(users_and_books), 200) if users_and_books else (
            jsonify({"message": "No users or books found"}), 404)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
