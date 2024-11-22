from bson.objectid import ObjectId
from models.connect_to_mongo import mongo_collection

def save_book_test_to_mongo(book_text) -> str:
    """
    Сохраняет текст книги в MongoDB и возвращает id
    :param book_text:
    """

    result = mongo_collection.insert_one({"text": book_text})
    return str(result.inserted_id)


def get_book_text_from_mongo(book_text_id) -> str | None:
    """
    Получаем текст книги из MongoDB
    :param book_text_id:
    :return: str
    """

    document = mongo_collection.find_one({"_id": ObjectId(book_text_id)})
    return document["text"] if document else None
