from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from models.create_user_table import User
sing_in_site_bp = Blueprint("sing_in", __name__)
sing_out_site_bp = Blueprint("sing_out", __name__)


@sing_in_site_bp.route("/sing_in", methods=["GET", "POST"])
def route_sing_in():
    print("переход на sing_in.html")

    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        print(f"Логин: {login}, Пароль: {password}")

        try:
            # Попробуем найти пользователя с таким логином и паролем
            user = User.get(User.login == login, User.password == password)
            print("Пользователь найден:", user)
            session["user_id"] = user.id
            session["username"] = user.first_name
            flash("Успешный вход в аккаунт")
            return redirect(url_for("home.route_home"))
        except User.DoesNotExist:
            # Вывод сообщения, если пользователь не найден
            print("Неверный логин или пароль")
            return render_template("sing_in.html", error="invalid_credentials")
        except Exception as e:
            # Обработка других исключений
            print("Общее исключение:", e)
            return render_template("sing_in.html", error="general_error")

    return render_template("sing_in.html")

@sing_in_site_bp.route("/sing_out")
def route_sing_out():
    session.pop("user_id", None)
    session.pop("username", None)
    flash("Вы вышли из аккаунта.")
    return redirect(url_for("home.route_home"))

