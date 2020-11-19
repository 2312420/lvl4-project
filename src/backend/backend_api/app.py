from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from extensions import db
import json
from datetime import datetime
import psycopg2


from models import Article


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
    return 'gets Sources'


@app.route('/sources', methods=['POST'])
def add_source():
    return 'adds source'


@app.route('/sources/<source_id>', methods=['DELETE'])
def delete_source(source_id):
    return source_id


# <!---- Article calls ----!> #

@app.route('/article', methods=['POST'])
def add_article():

    content = request.get_json()
    to_add = Article(content['id'], content['data'])
    db.session.add(to_add)
    db.session.commit()
    return "adds Article"

@app.route('/sources', methods=['PUT'])
def update_article():
    return 'updates article'


@app.route('/article/<article_id>', methods=['GET'])
def get_article(article_id):
    return article_id


@app.route('/article/<article_id>', methods=['DELETE'])
def delete_article(article_id):
    return article_id


@app.route('/article/<article_id>/context', methods=['PUT'])
def update_article_context(article_id):
    return article_id


@app.route('/article/findByStatus', methods=['GET'])
def find_article_by_status():
    return 'finds article by status'


# <!---- Sentence calls ----!> #

@app.route('/sentence', methods=['POST'])
def add_sentence():
    return 'adds sentence'


@app.route('/sentence/findByStatus', methods=['GET'])
def find_sentence_by_status():
    return 'finds sentence by status'


@app.route('/sentence/<sentence_id>/context', methods=['POST'])
def update_sentence_context(sentence_id):
    return sentence_id


@app.route('/sentence/<sentence_id>/sentiment', methods=['POST'])
def update_sentence_sentiment(sentence_id):
    return sentence_id


# <!---- Company calls ----!> #

@app.route('/company', methods=['POST'])
def add_company():
    return 'adds company'


@app.route('/company/<stock_code>/articles', methods=['GET'])
def get_company_articles(stock_code):
    return stock_code


@app.route('/company/<stock_code>/sentences', methods=['POST'])
def get_company_sentences(stock_code):
    return stock_code


if __name__ == '__main__':
    app.run()
