from models.create_book_table import Book
from flask import jsonify, Blueprint
from models.create_author_table import Author
from models.create_user_table import User

api_get_all_users_and_their_books_bp = Blueprint('get_users_and_their_books', __name__)

@api_get_all_users_and_their_books_bp.route('/api/get_all_users_and_books', methods=['GET'])
def get_all_users_and_books():
    """
    Получает список всех пользователей и их книг из базы данных.
    ---
    tags:
      - Users
    responses:
      200:
        description: Успешный ответ с массивом всех пользователей и их книг.
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
                  first_name:
                    type: string
                    example: "Иван"
                  last_name:
                    type: string
                    example: "Иванов"
                  books:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                          example: 10
                        book_name:
                          type: string
                          example: "Война и мир"
                        book_text:
                          type: string
                          example: "Текст книги или URL"
                        author:
                          type: string
                          example: "Лев Толстой"
                        time_added:
                          type: string
                          example: "2024-11-19T15:34:45"
      404:
        description: Пользователи или книги не найдены.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "No users or books found"
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
