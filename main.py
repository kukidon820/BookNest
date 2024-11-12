from flask import Flask
from routes.route_add_book import add_book_site_bp
from routes.route_home import home_site_bp
from routes.route_sing_in import sing_in_site_bp, sing_out_site_bp
from models.add_all_tables_in_database import create_tables
from routes.route_sing_up import sing_up_site_bp
from routes.route_update_book import update_book_site_bp
from routes.route_delete_book import delete_book_bp
from api.api_for_get_book_by_id import api_get_book_by_id_bp
from api.api_get_all_books import api_get_all_books_bp
from api.api_get_user_by_id import api_get_user_by_id_bp
from api.api_get_all_users_and_their_books import api_get_all_users_and_their_books_bp

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(delete_book_bp, url_prefix="/")
app.register_blueprint(update_book_site_bp, url_prefix='/')
app.register_blueprint(sing_out_site_bp, url_prefix='/')
app.register_blueprint(add_book_site_bp, url_prefix='/')
app.register_blueprint(home_site_bp, url_prefix='/')
app.register_blueprint(sing_up_site_bp, url_prefix='/')
app.register_blueprint(sing_in_site_bp, url_prefix='/')
app.register_blueprint(api_get_book_by_id_bp, url_prefix='/')
app.register_blueprint(api_get_user_by_id_bp, url_prefix="/")
app.register_blueprint(api_get_all_books_bp, url_prefix='/')
app.register_blueprint(api_get_all_users_and_their_books_bp, url_prefix="/")

with app.app_context():
    create_tables()

if __name__ == "__main__":
    app.run(debug=True)
