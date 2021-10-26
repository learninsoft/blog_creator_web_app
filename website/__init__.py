import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

from website.config import Config


db = SQLAlchemy()


def create_site():
    app = Flask(__name__)

    from .applications.blog import views as blog_views
    from .applications.errors import views as err_views
    from .applications.base import views

    app.register_blueprint(blog_views.blogs, url_prefix='/blogs')
    app.register_blueprint(views.base, url_prefix='/')
    app.register_blueprint(err_views.err_views)

    # from .applications.blog.models import Post

    if Config.DB_TYPE in ('sqlite'):
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
        db.init_app(app)
        create_database(app)
    # db.create_all(app=app)
    # migrate = Migrate(app, db)

    return app


def create_database(app):
    if not os.path.exists(f"{Config.DB_NAME}"):
        db.create_all(app=app)
        print("Database is created. ")
