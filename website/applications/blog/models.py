from datetime import datetime
from website import db

from website.applications.utils.logger import Logger


log_obj = Logger(name=__name__).logger


class Post(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)

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
            db.session.add(self)
            db.session.commit()
            log_obj.info("Successfully saved the post")
            return self.to_dict()
        except Exception as exc:
            log_obj.exception("Error occurred while saving the post", exc_info=True)
            raise Exception(exc)

    def to_dict(self):
        return {"id": self._id, "title": self.title, "slug": self.slug}
