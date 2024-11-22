from flask import render_template, Blueprint, request
from models.connect_to_mongo import mongo_collection
from bson.objectid import ObjectId

read_book_bp = Blueprint('read_book', __name__)

# Длина одного фрагмента текста
TEXT_CHUNK_SIZE = 5000  # 5000 символов на страницу


def get_chunk_text(full_text, chunk_number):
    if chunk_number == 1:
        start = 0
        end = chunk_number * TEXT_CHUNK_SIZE
        chunk = full_text[start:end]
    else:
        start = chunk_number * TEXT_CHUNK_SIZE
        end = start + TEXT_CHUNK_SIZE
        chunk = full_text[start:end]

    # Если последний символ не пробел, то ищем ближайший пробел и обрезаем текст до него
    if chunk and chunk[-1] != ' ':
        end = full_text.find(' ', end)
        if end == -1:
            end = len(full_text)
        chunk = full_text[start:end]

    return chunk, start, end


@read_book_bp.route('/read_book', methods=['GET'])
def read_book():
    book_text_id = request.args.get("book_text_id")
    chunk_number = request.args.get("chunk_number", 1, type=int)
    page = request.args.get("page", type=int)

    # Проверка наличия book_text_id
    if not book_text_id:
        return "Не указан ID книги", 400

    # Получаем текст книги
    book_text = mongo_collection.find_one({"_id": ObjectId(book_text_id)})

    if not book_text:
        return "Текст книги не найден", 404

    full_text = book_text['text']

    # Если указан номер страницы, используем его для вычисления chunk
    if page and page > 0:
        chunk, start, end = get_chunk_text(full_text, page)
        chunk_number = page
    else:
        chunk, start, end = get_chunk_text(full_text, chunk_number)

    # Проверяем, есть ли следующая и предыдущая часть
    next_chunk_number = chunk_number + 1 if end < len(full_text) else None
    prev_chunk_number = chunk_number - 1 if chunk_number > 1 else None

    # Индексация страницы: показываем номер страницы на основе chunk_number
    current_page_number = page if page else chunk_number

    return render_template("read_book.html",
                           chunk=chunk,
                           book_text_id=book_text_id,
                           chunk_number=chunk_number,
                           current_page_number=current_page_number,
                           next_chunk_number=next_chunk_number,
                           prev_chunk_number=prev_chunk_number)
