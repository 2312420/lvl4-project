from extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
import json

class Source(db.Model):
    __tablename__ = 'source'

    id = db.Column(db.Integer, primary_key=True)
    short_hand = db.Column(db.String())
    rss = db.Column(db.String())

    def __init__(self, short_hand, rss):
        self.short_hand = short_hand
        self.rss = rss

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'short_hand': self.short_hand,
            'rss': self.rss,
        }

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
    status = db.Column(db.String())
    source_id = db.Column(db.String())

    date = db.Column(db.String())
    time = db.Column(db.String())

    def __init__(self, id, title, transcript, source_id):
        self.id = id
        self.title = title
        self.transcript = transcript
        self.date = datetime.now()
        self.time = datetime.now()
        self.source_id = source_id
        self.status = ""

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'transcript': self.transcript,
            'date': self.date.strftime("%m/%d/%Y"),
            'time': self.time.strftime("%H:%M:%S"),
            'source_id': self.source_id,
            'status': self.status
        }


class Sentence(db.Model):
    __tablename__ = 'sentence'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String())
    sentiment = db.Column(db.Integer())
    status = db.Column(db.String())

    article_id = db.Column(db.Integer(), db.ForeignKey('article.id'))
    context = db.Column(db.String(), db.ForeignKey("company.stock_code"))

    def __init__(self, text, article_id):
        #self.id = id
        self.text = text
        self.article_id = article_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'sentiment': self.sentiment,
            'status': self.status
        }
