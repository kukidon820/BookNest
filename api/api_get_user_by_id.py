from flask import jsonify, request, Blueprint
from models.create_user_table import User


api_get_user_by_id_bp = Blueprint('get_user_by_id', __name__)


@api_get_user_by_id_bp.route('/api/get_user_by_id', methods=['GET'])
def get_user_by_id():
    """
    Получает информацию о пользователе по его уникальному идентификатору.
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              user_id:
                type: integer
                example: 1
                description: Уникальный идентификатор пользователя
    responses:
      200:
        description: Успешный ответ с информацией о пользователе.
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
      400:
        description: Идентификатор пользователя не указан.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "user_id is required"
      404:
        description: Пользователь не найден.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User not found"
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

    if 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400

    user_id = data['user_id']

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
        return jsonify({'message': 'User not found'}), 404
