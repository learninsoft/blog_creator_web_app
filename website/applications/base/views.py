import os

from flask import Blueprint
from flask import render_template
from flask.helpers import url_for
from werkzeug.utils import redirect

from website.applications.utils.logger import Logger
from website.config import Config

base = Blueprint('base', __name__)
log_obj = Logger(name=__name__).logger


@base.route("/")
def home_view():
    """
    The base route, which will redirect to blogs home page
    :return: redirecting to blogs home page
    """
    log_obj.info("Redirecting Home View to blogs page. ")
    return redirect(url_for('blogs.home_view'))


@base.route("/log/view/<string:key>")
def view_log(key):
    if key == "mlpqazoknwsx":
        with open(Config.LOGFILE, "r") as infile:
            log_contents = infile.readlines()[::-1]
        return render_template("base/view_log.html", log_contents=log_contents)
    else:
        LOG_SECRET_KEY = os.environ.get('LOG_SECRET_KEY', None)
        log_obj.info(f"Log secret key value: {LOG_SECRET_KEY}")
        return render_template("base/view_log.html", log_contents=[])
