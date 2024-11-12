from flask import jsonify, request, Blueprint
from models.create_user_table import User

api_get_user_by_id_bp = Blueprint('get_user_by_id', __name__)


@api_get_user_by_id_bp.route('/api/get_user_by_id', methods=['GET'])
def get_user_by_id():
    """
        Получает информацию о пользователе по его уникальному идентификатору.

        Возвращает:
            - Если пользователь найден:
                Возвращает JSON-массив с информацией о пользователе и статусом 200.
                Структура возвращаемого объекта пользователя:
                [
                    {
                        "id": int,                   # Уникальный идентификатор пользователя
                        "first_name": str,           # Имя пользователя
                        "last_name": str             # Фамилия пользователя
                    }
                ]

            - Если идентификатор пользователя не указан в запросе:
                Возвращает JSON с сообщением об ошибке и статусом 400.
                Пример: {"error": "user_id is required"}

            - Если пользователь не найден:
                Возвращает JSON с сообщением об отсутствии пользователя и статусом 404.
                Пример: {"message": "User not found"}

            - В случае любой ошибки при выполнении запроса:
                Возвращает JSON с сообщением об ошибке и статусом 500.
                Пример: {"error": "Описание ошибки"}

        Пример запроса:
            GET /api/get_user_by_id
            {
                "user_id": 1
            }
        """

    data = request.get_json()

    if 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400

    user_id = data['user_id']

    print("user_id: ", user_id)
    try:
        user = User.get(User.id == user_id)
    except User.DoesNotExist:
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    request_to = []

    if user:
        user_info = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        request_to.append(user_info)

        return jsonify(request_to), 200
    else:
        return jsonify({'message': 'Book not found'}), 404
