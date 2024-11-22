from models.create_book_table import Book
from flask import jsonify, Blueprint
from models.create_author_table import Author

api_get_all_books_bp = Blueprint('get_all_books', __name__)

@api_get_all_books_bp.route('/api/get_all_books', methods=['GET'])
def get_all_books():
    """
    Получает список всех книг из базы данных вместе с их авторами.
    ---
    tags:
      - Books
    responses:
      200:
        description: Успешный ответ с массивом всех книг.
        content:
          application/json:
            schema:
              type: array
              items:
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
      404:
        description: Книги не найдены.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Not found books"
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
    books = Book.select().join(Author)

    try:
        if books:
            books_list = []
            for book in books:
                books_list.append({
                    'id': book.id,
                    'book_name': book.book_name,
                    'book_text': book.book_text,
                    'author': book.author_id.first_name + ' ' + book.author_id.last_name,
                    'time_added': book.time_added
                })
            return jsonify(books_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({"Not found books"}), 404

