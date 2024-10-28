from flask import Flask
from routes.route_add_book import add_book_site_bp
from routes.route_home import home_site_bp
from routes.route_sing_in import sing_in_site_bp, sing_out_site_bp
from models.add_all_tables_in_database import create_tables
from routes.route_sing_up import sing_up_site_bp
from routes.route_update_book import update_book_site_bp

import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(update_book_site_bp, url_prefix='/')
app.register_blueprint(sing_out_site_bp, url_prefix='/')
app.register_blueprint(add_book_site_bp, url_prefix='/')
app.register_blueprint(home_site_bp, url_prefix='/')
app.register_blueprint(sing_in_site_bp, url_prefix='/')
app.register_blueprint(sing_up_site_bp, url_prefix='/')

with app.app_context():
    create_tables()

if __name__ == "__main__":
    app.run(debug=True)
