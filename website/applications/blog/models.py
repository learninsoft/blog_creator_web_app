from datetime import datetime
from website import db


log_obj = Logger(name=__name__).logger

class Post(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean,default=True)

    def validate(self):
        try:
            assert len(self.title) > 3, "Title must be greater than 3 characters"
        except AssertionError as aser:
            log_obj.exception("Error occurred", exc_info=True)
            raise AssertionError(aser)

    def save(self):
        self.validate()
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {"id":self._id, "title": self.title, "slug":self.slug}
