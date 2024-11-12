from models.create_book_table import Book
from flask import jsonify, Blueprint
from models.create_author_table import Author

api_get_all_books_bp = Blueprint('get_all_books', __name__)

@api_get_all_books_bp.route('/api/get_all_books', methods=['GET'])
def get_all_books():
    """
       Получает список всех книг из базы данных вместе с их авторами.

       Возвращает:
           - Если книги найдены:
               Возвращает JSON-массив с информацией о всех книгах и статусом 200.
               Каждый объект книги имеет следующую структуру:
               {
                   "id": int,                    Уникальный идентификатор книги
                   "book_name": str,             Название книги
                   "book_text": str,             Текст книги (URL или текстовый контент)
                   "author": str,                Имя и фамилия автора книги
                   "time_added": str             Дата и время добавления книги
               }

           - Если книги не найдены:
               Возвращает JSON с сообщением об отсутствии книг и статусом 404.
               Пример: {"Not found books"}

           - В случае любой ошибки при выполнении запроса:
               Возвращает JSON с сообщением об ошибке и статусом 500.
               Пример: {"error": "Описание ошибки"}

       Пример запроса:
           GET /api/get_all_books
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
