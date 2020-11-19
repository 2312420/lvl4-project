from extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


class Source(db.Model):
    __tablename__ = 'source'

    id = db.Column(db.Integer, primary_key=True)
    short_hand = db.Column(db.String())
    rss = db.Column(db.String())

    def __init__(self, id, short_hand, rss):
        self.id = id
        self.short_hand = short_hand
        self.rss = rss

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Company(db.Model):
    __tablename__ = 'company'

    stock_code = db.Column(db.String, primary_key=True)
    short_hand = db.Column(db.String)

    def __init__(self, stock_code, short_hand, rss):
        self.stock_code = stock_code
        self.short_hand = short_hand

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    transcript = db.Column(db.String())
    date = db.Column(db.String())
    status = db.Column(db.String())

    source = db.Column(db.String())
    sentences = db.relationship("Sentence")

    def __init__(self, id, title, transcript):
        self.id = id
        self.title = title
        self.transcript = transcript
        self.date = datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Sentence(db.Model):
    __tablename__ = 'sentence'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String())
    sentiment = db.Column(db.Integer())
    status = db.Column(db.Integer())

    article_id = db.Column(db.Integer(), db.ForeignKey('article.id'))
    context = db.Column(db.String(), db.ForeignKey("company.stock_code"))

    def __init__(self, id, text, article_id):
        self.id = id
        self.title = text
        self.text = text
        self.article_id = article_id

    def __repr__(self):
        return '<id {}>'.format(self.id)