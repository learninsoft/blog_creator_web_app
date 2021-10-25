from flask import Blueprint, render_template

from website.applications.utils.logger import Logger


log_obj = Logger(name=__name__).logger
err_views = Blueprint('errors', __name__)


@err_views.app_errorhandler(404)
def custom_404(msg):
    log_obj.info(f"404 Page not found, {msg}")
    return f"the requested page is not found\n\n{msg}", 404


@err_views.app_errorhandler(500)
def custom_500(msg):
    log_obj.info(f"500 Internal error, {msg}")
    return "Internal Error, Please try after some time, Report it to team.", 500
