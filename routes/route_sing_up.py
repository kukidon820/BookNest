from flask import render_template, Blueprint, request, flash, redirect, url_for, session
from models.create_user_table import User
from peewee import IntegrityError

sing_up_site_bp = Blueprint("sing_up", __name__)


@sing_up_site_bp.route("/sing_up", methods=["GET", "POST"])
def route_sing_up():
    """
        Обрабатывает регистрацию нового пользователя.

        Если метод запроса - POST, функция выполняет следующие действия:
        1. Извлекает логин, имя, фамилию, пароль и подтверждение пароля из формы.
        2. Проверяет, совпадают ли введенные пароли.
        3. Если пароли совпадают, создает нового пользователя и сохраняет его в базе данных.
        4. Устанавливает идентификатор и имя пользователя в сессии, отображает сообщение об успешной регистрации и
           перенаправляет на главную страницу.
        5. Если логин уже существует, возвращает сообщение об ошибке и отображает форму регистрации.
        6. Обрабатывает другие исключения и отображает соответствующее сообщение об ошибке.

        Если метод запроса - GET, функция отображает страницу регистрации (`sing_up.html`).

        Возвращает:
            - HTML-шаблон страницы регистрации (`sing_up.html`) с возможным сообщением об ошибке,
              или перенаправляет на главную страницу после успешной регистрации.

        Пример запроса:
            GET /sing_up
            POST /sing_up (с логином, именем, фамилией и паролем в теле запроса)
    """

    print("переход на sing_up.html")

    if request.method == "POST":
        login = request.form.get("login")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Проверка совпадения паролей
        if password != confirm_password:
            return render_template("sing_up.html", error="password_mismatch")

        try:
            # Создаем пользователя и сохраняем в базе данных
            user = User.create(
                login=login,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            flash("Регистрация прошла успешно")

            # Сохраняем идентификатор пользователя и имя в сессии
            session["user_id"] = user.id  # Используем id созданного пользователя
            session["username"] = user.first_name  # Используем имя созданного пользователя

            return redirect(url_for("home.route_home"))  # Убедитесь, что маршрут указан верно

        except IntegrityError:
            # Исключение уникальности логина
            print("Ошибка: логин уже существует.")
            return render_template("sing_up.html", error="login_taken")
        except Exception as e:
            # Общее исключение с выводом ошибки
            print(f"Общее исключение: {e}")  # Вывод ошибки в консоль для отладки
            return render_template("sing_up.html", error="general_error")

    return render_template("sing_up.html")

