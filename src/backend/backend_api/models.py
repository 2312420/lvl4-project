from extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
import json
import hashlib


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

    def __init__(self, stock_code, short_hand):
        self.stock_code = stock_code
        self.short_hand = short_hand

    def __repr__(self):
        return '<stock_code {}>'.format(self.stock_code)

    def serialize(self):
        return {
            'stock_code': self.stock_code,
            'short_hand': self.short_hand
        }


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    transcript = db.Column(db.String())
    status = db.Column(db.String())
    source_id = db.Column(db.String())
    context = db.Column(db.ARRAY(db.String()))

    date = db.Column(db.String())
    time = db.Column(db.String())

    # def __init__(self, title, transcript, source_id, date, time):
    def __init__(self, *args):
        self.title = args[0]
        self.transcript = args[1]
        self.source_id = args[2]
        self.status = "CONTEXT"
        self.id = self.hash()
        self.context = []

        if len(args) > 3:
            self.date = self.time = datetime.strptime(args[3], '%m/%d/%Y, %H:%M:%S')
        else:
            self.date = datetime.now()
            self.time = datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def hash(self):
        title = self.title
        transcript = self.transcript.split()
        first_word = transcript[0]
        last_word = transcript[-1]
        hash_string = first_word + title + last_word
        hash_obj = hashlib.md5(hash_string.encode())
        return hash_obj.hexdigest()

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'transcript': self.transcript,
            'date': self.date.strftime("%m/%d/%Y"),
            'time': self.time.strftime("%H:%M:%S"),
            'source_id': self.source_id,
            'status': self.status,
            'context': self.context
        }


class Sentence(db.Model):
    __tablename__ = 'sentence'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String())
    sentiment = db.Column(db.Float())
    status = db.Column(db.String()) #CONTEXT, SENTIMENT, DONE
    date = db.Column(db.String())
    time = db.Column(db.String())

    article_id = db.Column(db.Integer(), db.ForeignKey('article.id'))
    context = db.Column(db.String(), db.ForeignKey("company.stock_code"))


    def __init__(self, text, article_id, date, time):
        #self.id = id
        self.text = text
        self.article_id = article_id
        self.status = "CONTEXT"
        self.date = self.time = datetime.strptime(date, '%m/%d/%Y')
        self.time = datetime.strptime(time, '%H:%M:%S')

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'sentiment': self.sentiment,
            'status': self.status,
            'article_id': self.article_id,
            'date': self.date.strftime("%m/%d/%Y"),
            'time': self.time.strftime("%H:%M:%S"),
        }
