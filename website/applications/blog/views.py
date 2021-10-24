import json
from flask import flash, Blueprint, render_template, request, jsonify, make_response
from .models import Post

from website import db
from website.applications.utils.logger import Logger


log_obj = Logger(name=__name__).logger
blogs = Blueprint('blogs', __name__)


@blogs.route("/")
def home_view():
    log_obj.info("Rendering the blog home page")
    # posts = query(Post).filter(something).limit(5).all()
    posts = Post.query.filter(Post._id>15,Post.slug.startswith('H')).order_by(Post._id.desc()).limit(3)
    return render_template("blog/home.html", posts=posts)


@blogs.route("/create", methods=["GET", "POST"])
def create_post():
    log_obj.info("STARTing the function")
    try:
        # cookie_val = request.cookies.get('learning')
        is_post_created = False
        err_message = None
        log_obj.debug(f"Request method: {request.method}")
        log_obj.info(f"Client IP address: {request.remote_addr}")
        if request.method == "POST":
            post = dict(request.form)
            log_obj.debug(f"{post}")
            log_obj.info("Creating the post")
            new_post = Post(**post)
            log_obj.info("Saving the post to Database")
            new_post.save()
            if new_post._id:
                is_post_created = True
        else:
            log_obj.info("Displaying the Page to create the post")
    except AssertionError as aser:
        log_obj.exception("AssertionError in the fields", exc_info=True)
        err_message = str(aser)
    except Exception as exc:
        log_obj.exception("error occurred", exc_info=True)
        err_message = str(exc)
    finally:
        if is_post_created:
            log_obj.info("The post is created successfully. ")
            return jsonify(new_post.to_dict())
        # if cookie_val:
        #     err_message = cookie_val
        log_obj.info("Rendering the page: --> blog/create.html")
        resp = make_response(render_template(render_template("blog/create.html",err_message=err_message)))
        resp.set_cookie("learning", "cookieTest")
        return resp


@blogs.route("/view/<int:id>")
def view_post(id):
    try:
        post = {}
        post = Post.query.get(id)
    except:
        log_obj.error("Error occurred", exc_info=True)
    resp = make_response(render_template("blog/view.html", post=post))
    resp.set_cookie("learning", "cookieTest")
    return resp
#
# @blogs.route("/view/<string:slug>")
# def view_post(slug):
#     try:
#         post = {}
#         post = Post.query.filter_by(slug=slug).first()
#     except:
#         log_obj.error("Error occurred", exc_info=True)
#     return render_template("blog/view.html", post=post)
