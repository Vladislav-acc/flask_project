from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from tzlocal import get_localzone
import pytz
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_mail import Mail


db = SQLAlchemy()
DB_NAME = 'database.db'
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('DB_USER')
    app.config['MAIL_PASSWORD'] = {os.environ.get('DB_PASS')}
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    mail.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Post, Comment, Like

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    @app.context_processor
    def my_processor():

        def local_time(utc_time):
            local_tz = get_localzone()
            local_dt = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
            return datetime.strftime(local_dt, '%d.%m.%y %H:%M')

        return dict(local_time=local_time)

    return app


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Database created!')