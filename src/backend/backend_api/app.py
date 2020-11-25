from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from extensions import db
import json
from datetime import datetime
import psycopg2


from models import Company, Source, Article, Sentence


def register_extensions(app):
    db.init_app(app)


def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    return app


app = create_app('config.py')


@app.route('/')
def root():
    return render_template('index.html')


# <!---- Source calls ----!> #

@app.route('/sources', methods=['GET'])
def get_sources():
    try:
        sources = Source.query.all()
        if sources == None:
            return "400: No source found"
        else:
            to_return = []
            for source in sources:
                to_return.append(source.serialize())
            return to_return
    except:
        return "408: Unable to acess db"


@app.route('/sources', methods=['POST'])
def add_source():

    if request.is_json:
        try:
            content = request.get_json()
            to_add = Source(content['short_hand'], content['rss'])
            try:
                db.session.add(to_add)
                db.session.commit()
                return "201: item created"
            except:
                return "409: existing source already exists"

        except:
            return "400: Invalid input, object invalid"

    else:
        return "400: Invalid input, object invalid"


@app.route('/sources/<source_id>', methods=['DELETE'])
def delete_source(source_id):
    if request.is_json():
        try:
            content = request.get_json()
            source = Source.query.get(source_id)
            if source == None:
                return "404: Source not found"
            else:
                db.session.delete(source)
                db.session.commit()
                return "200: Source deleted"
        except:
            return "400: Invalid id supplied"
    else:
        return "405: Validation exception, JSON not provided"


# <!---- Article calls ----!> #

@app.route('/article', methods=['POST'])
def add_article():
    if request.is_json:
        try:
            content = request.get_json()
            to_add = Article(content['id'], content['title'], content['transcript'], content['source_id'])
            db.session.add(to_add)
            db.session.commit()
            return "200: added Article"
        except:
            return "400"
    else:
        return "405: Validation exception, JSON not provided"


@app.route('/update_article', methods=['PUT'])
def update_article():
    if request.is_json:
        try:
            content = request.get_json()
            article = Article.query.get(content['id'])
            article.title = content['title']
            article.transcript = content['transcript']
            db.session.commit()
            return "200: updated Article"
        except:
            return "400: Invalid id supplied"
    else:
        return "405: Validation exception, JSON not provided"


@app.route('/article/<article_id>', methods=['GET'])
def get_article(article_id):
    try:
        article = Article.query.get(article_id)
        if article == None:
            return "404: article not found"
        else:
            return json.dumps(article.serialize())
    except:
        return "405: Validation exception"


@app.route('/article/<article_id>', methods=['DELETE'])
def delete_article(article_id):
    if request.is_json():
        try:
            content = request.get_json()
            article = Article.query.get(article_id)
            if article == None:
                return "404: article not found"
            else:
                db.session.delete(article)
                db.session.commit()
                return "200: Article deleted"
        except:
            return "400: Invalid id supplied"
    else:
        return "405: Validation exception, JSON not provided"


@app.route('/article/<article_id>/context', methods=['PUT'])
def update_article_context(article_id):
    if request.is_json:
        try:
            content = request.get_json()
            article = Article.query.get(article_id)
            if article == None:
                return "404: article not found"
            else:
                article.title = content['context']
                db.session.commit()
                return "200: updated article"
        except:
            return "400: Invalid id supplied"
    else:
        return "405: Validation exception, JSON not provided"


@app.route('/article/<article_id>/status', methods=['PUT'])
def update_article_status(article_id):
    if request.is_json:
        try:
            content = request.get_json()
            article = Article.query.get(article_id)
            if article == None:
                return "404: article not found"
            else:
                article.title = content['status']
                db.session.commit()
            return "200: updated article status"
        except:
            return "400: Invalid id supplied"
    else:
        return "405: Validation exception, JSON not provided"


@app.route('/article/findByStatus', methods=['GET'])
def find_article_by_status():
    if request.is_json():
        try:
            content = request.get_json()
            articles = Article.query.filter_by(status= content['status'])
            output = []
            for article in articles:
                output.append(article.serialize())
            return json.dumps(output)
        except:
            return "400: Invalid status value"
    else:
        return "405: Validation exception, JSON not provided"


# <!---- Sentence calls ----!> #

@app.route('/sentence', methods=['POST'])
def add_sentence():
    if request.is_json:
        try:
            content = request.get_json()
            to_add = Sentence(content['text'], content['article_id'])
            db.session.add(to_add)
            db.session.commit()
            return "201: item created"
        except:
            return "400: Invalid input, object invalid"
    else:
        return "400: Invalid input, object invalid"


@app.route('/sentence/findByStatus', methods=['GET'])
def find_sentence_by_status():
    if request.is_json():
        try:
            content = request.get_json()
            sentences = Sentence.query.filter_by(status=content['status'])
            output = []
            for sentence in sentences:
                output.append(sentence.serialize())
            return json.dumps(output)
        except:
            return "400: Invalid status value"
    else:
        return "405: Validation exception, JSON not provided"


@app.route('/sentence/<sentence_id>/context', methods=['POST'])
def update_sentence_context(sentence_id):
    if request.is_json:
        try:
            content = request.get_json()
            sentence = Source.query.get(sentence_id)
            if sentence == None:
                return "404: article not found"
            else:
                sentence.title = content['context']
                db.session.commit()
                return "200: updated article"
        except:
            return "400: Invalid id supplied"
    else:
        return "405: Validation exception, JSON not provided"


@app.route('/sentence/<sentence_id>/sentiment', methods=['POST'])
def update_sentence_sentiment(sentence_id):
    if request.is_json:
        try:
            content = request.get_json()
            sentence = Source.query.get(sentence_id)
            if sentence == None:
                return "404: article not found"
            else:
                sentence.title = content['sentiment']
                db.session.commit()
                return "200: updated article"
        except:
            return "400: Invalid id supplied"
    else:
        return "405: Validation exception, JSON not provided"


# <!---- Company calls ----!> #


@app.route('/company', methods=['POST'])
def add_company():
    if request.is_json:
        try:
            content = request.get_json()
            to_add = Company(content['stock_code'], content['short_hand'])
            try:
                db.session.add(to_add)
                db.session.commit()
                return "201: item created"
            except:
                return "409: Existing company already exists"
        except:
            return "400: Invalid input, object invalid"
    else:
        return "400: Invalid input, object invalid"


@app.route('/company/<stock_code>', methods=['GET'])
def get_company(stock_code):
    try:
        company = Company.query.get(stock_code)
        if company == None:
            return "404: article not found"
        else:
            return json.dumps(company.serialize())
    except:
        return "405: Validation exception"


@app.route('/company/<stock_code>/sentences', methods=['GET'])
def get_company_sentences(stock_code):
    try:
        sentences = Sentence.query.filter_by(context=stock_code).all()
        if sentences == []:
            return "404: No sentences found"
        else:
            output = []
            for sentence in sentences:
                output.append(sentence.serialize())
            return json.dumps(output)
    except:
        return "400: Invalid Input"


if __name__ == '__main__':
    app.run()
