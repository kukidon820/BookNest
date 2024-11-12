from models.create_book_table import Book
from flask import jsonify, request, Blueprint
from models.create_author_table import Author

api_get_book_by_id_bp = Blueprint('get_book_by_id', __name__)

@api_get_book_by_id_bp.route('/api/get_book_by_id', methods=['GET'])
def get_book_by_id():

    """
        Получает информацию о книге по её уникальному идентификатору (ID).

        Запрос ожидает JSON с параметром:
            - book_id (int): уникальный идентификатор книги, которую нужно найти.

        Возвращает:
            - Если book_id не указан в запросе:
                Возвращает JSON с сообщением об ошибке и статусом 400.
                Пример: {"error": "book_id is required"}

            - Если книга с указанным book_id не найдена:
                Возвращает JSON с сообщением об отсутствии книги и статусом 404.
                Пример: {"message": "Book not found"}

            - Если книга найдена:
                Возвращает JSON с информацией о книге и статусом 200.
                Структура JSON:
                {
                    "id": int,                   # ID книги
                    "book_name": str,            # Название книги
                    "book_text": str,            # Текст книги (URL или текстовый контент)
                    "author": str,               # Имя и фамилия автора
                    "time_added": str            # Дата и время добавления книги
                }

            - В случае любой другой ошибки:
                Возвращает JSON с сообщением об ошибке и статусом 500.
                Пример: {"error": "Описание ошибки"}

        Исключения:
            - Book.DoesNotExist: Если книга с указанным book_id отсутствует в базе данных.
            - Exception: Для любых других ошибок при выполнении запроса.

        Пример запроса:
            GET /api/get_book_by_id
            {
                "book_id": 1
            }
        """

    data = request.get_json()

    if 'book_id' not in data:
        return jsonify({'error': 'book_id is required'}), 400

    book_id = data['book_id']

    try:
        book = Book.select().where(Book.id == book_id).join(Author).get()
    except Book.DoesNotExist:
        return jsonify({'message': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if book:
        request_to = {
            'id': book_id,
            'book_name': book.book_name,
            'book_text': book.book_text,
            'author': book.author_id.first_name + ' ' + book.author_id.last_name,
            'time_added': book.time_added
        }
        return jsonify(request_to), 200
    else:
        return jsonify({'message': 'Book not found'}), 404


