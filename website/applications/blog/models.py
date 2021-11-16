import re

from datetime import datetime
from website import db

from website.applications.utils.logger import Logger


log_obj = Logger(name=__name__).logger


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post._id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag._id')),
                     )


class Post(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts'), lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self._generate_slug()

    def _generate_slug(self):
        self.slug = slugify(self.title)

    def validate(self):
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
        try:
            self.validate()
            # create tag object, and append it to post
            # new_post.tags.append(tag_obj1)
            db.session.add(self)
            db.session.commit()
            log_obj.info("Successfully saved the post")
            return self.to_dict()
        except Exception as exc:
            log_obj.exception("Error occurred while saving the post", exc_info=True)
            raise Exception(exc)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "slug": self.slug}

    @property
    def id(self):
        return self._id


class Tag(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))

    def save(self):
        db.session.add(self)
        db.session.commit()
