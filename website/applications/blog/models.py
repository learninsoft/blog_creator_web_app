import re
import time

from datetime import datetime

import sqlalchemy

from website import db
from website.applications.utils.logger import Logger
# from website.applications.blog.helpers import slugify

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


class Post(db.Model):
    """
    The blog post class, which contains all the attributes and methods
    """
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(180), unique=True)
    slug_type = db.Column(db.String(10))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)
    category = db.Column(db.String(300), default="default")

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self._generate_slug()
        self._process_body()

    def _process_body(self):
        """
        removes all the extra information from the body
        :return: processed body
        """
        log_obj.info("Processing the body of the post: ")
        self.body = f'<div class={self.body.split("<div class=")[1]}'.replace(
            'class="ql-editor" data-gramm="false" contenteditable="true"', "")

    def _generate_slug(self):
        """
        generates the slug for the post based on the title, if slug is not there.
        :return:
        """
        if not self.slug or self.slug_type in ('auto',):
            log_obj.info("Generating the slug")
            self.slug = slugify(self.title) + "-" + str(time.time_ns())
        else:
            log_obj.info("slug entered value to clean slug")
            self.slug = slugify(self.slug)

    def validate(self):
        """
        this method will validate the post.
        :return:
        """
        log_obj.info("Validating the Post values. ")
        try:
            assert len(self.title) > 3, ("Title must be greater than 3 "
                                         "characters")
        except AssertionError as aser:
            log_obj.exception("Error occurred", exc_info=True)
            raise AssertionError(aser)
        except Exception as exc:
            log_obj.exception("Error occurred while validating the post", exc_info=True)
            raise Exception(exc)

    def save(self):
        """
        this method will save the post, to the database after successful validations.
        :return:
        """
        try:
            self.validate()
            db.session.add(self)
            db.session.commit()
            log_obj.info("Successfully saved the post")
            return self.to_dict()
        except sqlalchemy.exc.IntegrityError as integrity_err:
            log_obj.warning(f"{self.slug} already exists. ")
            log_obj.exception("error occurred integrity error sqlalchemy", exc_info=True)
            raise Exception(integrity_err)
        except Exception as exc:
            log_obj.exception("Error occurred while saving the post", exc_info=True)
            raise Exception(exc)

    def to_dict(self):
        """
        this method returns the dictionary with the necessary fields.
        :return:
        """
        log_obj.debug(f"Returning the dictionary for {self.id}")
        return {"id": self.id, "title": self.title, "slug": self.slug}

    @property
    def id(self):
        return self._id
