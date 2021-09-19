from flask import Flask


def create_site():
    app = Flask(__name__)

    from .applications import blog
    app.register_blueprint(blog.views.blogs, url_prefix='/')
    
    return app
