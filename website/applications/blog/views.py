from flask import Blueprint, render_template


blogs = Blueprint('blogs', __name__)


@blogs.route("/")
def blog_home_view():
    return render_template("blog/home.html")
