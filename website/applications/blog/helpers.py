import re
import werkzeug.exceptions

from .models import Post

from website.applications.utils.logger import Logger


log_obj = Logger(name=__name__).logger


def slugify(s):
    """
    replaces spaces with -
    :param s: input string
    :return: slug string with lowercase.
    """
    log_obj.info(f"Inside slugify: {s}")
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s).lower()


def slug_exists(slug_value):
    """
    Checks for whether slug_exists or not.
    :param slug_value: slug string to check.
    :return:
    """
    return_status = {'is_slug_exists': True, 'message': ""}
    try:
        log_obj.info(f"Slug Search parameters: {slug_value}")
        posts = Post.query.filter_by(slug=slugify(slug_value)).first()
        log_obj.info(f"Posts retrieved. with slug")
        if posts:
            return_status['message'] = f"Post Exists with the slug {slug_value} at {posts.id}"
            return_status['is_slug_exists'] = True
        else:
            return_status['is_slug_exists'] = False
    except werkzeug.exceptions.NotFound:
        log_obj.info("slug does not exists, can proceed to create the post. ")
        return_status['is_slug_exists'] = False
    except Exception:
        log_obj.error("Error occurred in is_slug_exists() ", exc_info=True)
    finally:
        log_obj.info(f"Exiting slug_exists: {return_status}")
        return return_status
