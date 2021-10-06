from flask import Flask


def create_site():
    app = Flask(__name__)

    from .applications.blog import views as blog_views
    from .applications.base import views

    app.register_blueprint(blog_views.blogs, url_prefix='/blogs')
    app.register_blueprint(views.base, url_prefix='/')

    return app
