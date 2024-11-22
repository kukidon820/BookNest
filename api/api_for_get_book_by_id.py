from models.create_book_table import Book
from flask import jsonify, request, Blueprint
from models.create_author_table import Author

api_get_book_by_id_bp = Blueprint('get_book_by_id', __name__)


@api_get_book_by_id_bp.route('/api/get_book_by_id', methods=['GET'])
def get_book_by_id():
    """
    Получает информацию о книге по её уникальному идентификатору (ID).
    ---
    tags:
      - Books
    parameters:
      - in: body
        name: body
        description: JSON с параметром book_id.
        required: true
        schema:
          type: object
          properties:
            book_id:
              type: integer
              example: 1
    responses:
      200:
        description: Успешный ответ с информацией о книге.
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                book_name:
                  type: string
                  example: "Название книги"
                book_text:
                  type: string
                  example: "Текст книги"
                author:
                  type: string
                  example: "Имя Фамилия"
                time_added:
                  type: string
                  example: "2024-11-19T15:34:45"
      400:
        description: Ошибка, если book_id отсутствует в запросе.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "book_id is required"
      404:
        description: Ошибка, если книга не найдена.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Book not found"
      500:
        description: Внутренняя ошибка сервера.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Описание ошибки"
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

