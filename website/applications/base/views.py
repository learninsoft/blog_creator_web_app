from flask import Blueprint
from flask.helpers import url_for
from werkzeug.utils import redirect


base = Blueprint('base', __name__)


@base.route("/")
def home_view():
    print("Home View")
    return redirect(url_for('blogs.home_view'))
