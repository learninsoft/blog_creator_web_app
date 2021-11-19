import json
import werkzeug.exceptions

from flask import (Blueprint, render_template, request, make_response,
                   abort, redirect, url_for, jsonify)

from .models import Post

from website.applications.utils.logger import Logger


log_obj = Logger(name=__name__).logger
blogs = Blueprint('blogs', __name__)


@blogs.route("/")
def home_view():
    """
    blog page home view
    :return:
    """
    log_obj.info("Rendering the blog home page")
    return render_template("blog/home.html")


@blogs.route("/create", methods=["GET", "POST"])
def create_post():
    """
    route for Creating the blog post
    :return:
    """
    log_obj.info("STARTing the function")
    is_post_created = False
    is_slug_exists = False
    err_message = ""
    try:
        # cookie_val = request.cookies.get('learning')
        log_obj.debug(f"Request method: {request.method}")
        log_obj.info(f"Client IP address: {request.remote_addr}")
        if request.method == "POST":
            post = json.loads(request.data)
            log_obj.debug(f"{post}")
            log_obj.info("Creating the post")
            new_post = Post(**post)
            log_obj.info("Saving the post to Database")
            new_post.save()
            if new_post.id:
                is_post_created = True
        else:
            log_obj.info("Displaying the Page to create the post")
    except AssertionError as aser:
        log_obj.exception("AssertionError in the fields", exc_info=True)
        err_message = str(aser)
    except Exception as exc:
        log_obj.exception("error occurred creating the post", exc_info=True)
        if "(sqlite3.IntegrityError)" in str(exc):
            is_slug_exists = True
        err_message = str(exc)
    finally:
        if err_message:
            err_message = "Something went wrong. Crosscheck the information, that you've entered"
        if is_slug_exists:
            log_obj.info("slug already exists")
            err_message = "Slug already exists. Please choose another one. "
        if is_post_created:
            log_obj.info("The post is created successfully. ")
            log_obj.info(f"New post created. {new_post.to_dict()}")
            rets = {**new_post.to_dict(), "redirect_to":url_for('blogs.published_view', post_info=json.dumps(new_post.to_dict()))}
            return make_response(jsonify(rets), 201)
            log_obj.info(f"{type(new_post)}")
            # return redirect(url_for("blogs.view_post", id=new_post.id))
            # return render_template("blog/published.html", blog=new_post.to_dict())
            #
            # return redirect(url_for('blogs.published_view',
            # post_info=json.dumps(new_post.to_dict())))
            # return redirect(url_for('blogs.published_view',  post=new_post))
            # return render_template("blog/published.html", blog=new_post, err_message=err_message)
        log_obj.info("Rendering the page: --> blog/create.html")
        resp = make_response(render_template("blog/create.html", err_message=err_message))
        resp.set_cookie("learning", "cookieTest")
        return resp


@blogs.route("/view/<int:id>")
def view_post(id):
    post = {}
    recent_posts = {}
    try:
        log_obj.info(f"Querying for id: {id}")
        post = Post.query.get_or_404(id)
        recent_posts = Post.query.order_by(Post._id.desc()).limit(3).all()
        log_obj.info(f"Total recent posts retrieved: {len(recent_posts)}")
        log_obj.info(f"Post id {post.id} retrieved successfully. ")

    except werkzeug.exceptions.NotFound:
        log_obj.warning(f"Querying for id: {id}, did not found")
        abort(404)
    except Exception:
        log_obj.error("Error occurred", exc_info=True)
    resp = make_response(render_template("blog/view.html", post=post, recent_posts=recent_posts))
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


@blogs.route("/instructions")
def instructions_view():
    """
    Instructions page view
    :return:
    """
    log_obj.info("Rendering the blog instructions page")
    return render_template("blog/instructions.html")


@blogs.route("/publish/<string:post_info>")
def published_view(**kwargs):
    """
    publish page, which will be shown after successful entry of the post.
    :param kwargs:
    :return:
    """
    log_obj.info("Rendering the page: --> blog/published.html")
    log_obj.info(f"{kwargs}")
    new_post = kwargs.get('post_info', {"id": 999, "title": "dummy", "slug": "dummy-slug"})
    log_obj.info(f"Post published: {new_post}")
    return render_template("blog/published.html", blog=json.loads(new_post))


@blogs.route("/all")
def view_all_posts():
    posts = {}
    try:
        posts = Post.query.all()
        log_obj.info(f"Total retrieved posts: {len(posts)}")
    except Exception:
        log_obj.error("Error occurred in view_all_posts() ", exc_info=True)
    return render_template("blog/all_view.html", posts=posts)


@blogs.route("/search")
def search_posts():
    posts = {}
    try:
        search_params = request.args.get("search_params", "welcome")
        log_obj.info(f"Search parameters: {search_params}")
        posts = Post.query.filter(Post.slug.startswith(search_params))\
            .order_by(Post._id.desc()).limit(9)
        log_obj.info(f"Posts retrieved. ")
    except Exception:
        log_obj.error("Error occurred in search_posts() ", exc_info=True)
    return render_template("blog/all_view.html", posts=posts)


@blogs.route("/about")
def about_page():
    log_obj.info("Rendering about us page. ")
    return render_template("blog/about_disclaimer.html", about=True)


@blogs.route("/disclaimer")
def disclaimer_page():
    log_obj.info("Rendering disclaimer page. ")
    return render_template("blog/about_disclaimer.html", disclaimer=True)
