from extensions import db
from sqlalchemy.dialects.postgresql import JSON


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.String(), primary_key=True)
    data = db.Column(JSON)

    def __init__(self, id, data):
        self.id = id
        self.data = data

    def __repr__(self):
        return '<id {}>'.format(self.id)
