from flask import Flask, render_template, request
from models import Company, Source, Article, Sentence
from flask_sqlalchemy import SQLAlchemy
import flask
from extensions import db
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Register database for api use
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

# <------------------------->
# <----- Source calls ------>
# <------------------------->

@app.route('/sources', methods=['GET'])
def get_sources():
    try:
        sources = Source.query.all()
        if sources == None:
            return flask.Response(status=400)
        else:
            to_return = []
            for source in sources:
                to_return.append(source.serialize())
            return json.dumps(to_return)
    except:
        return flask.Response(status=408)


@app.route('/sources', methods=['POST'])
def add_source():
    if request.is_json:
        try:
            content = request.get_json()
            to_add = Source(content['short_hand'], content['rss'])
            try:
                db.session.add(to_add)
                db.session.commit()
                return flask.Response(status=201)
            except:
                return flask.Response(status=409)

        except:
            return flask.Response(status=401)

    else:
        return flask.Response(status=400)


@app.route('/sources/<source_id>', methods=['DELETE'])
def delete_source(source_id):
    try:
        content = request.get_json()
        source = Source.query.get(source_id)
        if source == None:
            return flask.Response(status=404)
        else:
            db.session.delete(source)
            db.session.commit()
            return flask.Response(status=200)
    except:
        return flask.Response(status=400)

# <------------------------->
# <----- Article calls ----->
# <------------------------->

@app.route('/article', methods=['POST'])
def add_article():
    if request.is_json:
        try:
            content = request.get_json()
            to_add = Article(content['title'], content['transcript'], content['source_id'])
            db.session.add(to_add)
            db.session.commit()
            return flask.Response(status=200)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=405)


@app.route('/article_with_date', methods=['POST'])
def add_article_with_date():
    if request.is_json:
        try:
            content = request.get_json()
            to_add = Article(content['title'], content['transcript'], content['source_id'], content['date-time'])
            db.session.add(to_add)
            db.session.commit()
            return flask.Response(status=200)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=405)


@app.route('/update_article', methods=['PUT'])
def update_article():
    if request.is_json:
        try:
            content = request.get_json()
            article = Article.query.get(content['id'])
            article.title = content['title']
            article.transcript = content['transcript']
            db.session.commit()
            return flask.Response(status=200)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=405)


@app.route('/article/<article_id>', methods=['GET'])
def get_article(article_id):
    try:
        article = Article.query.get(article_id)
        if article == None:
            return flask.Response(status=404)
        else:
            return json.dumps(article.serialize())
    except:
        return flask.Response(status=405)


@app.route('/article/<article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        content = request.get_json()
        article = Article.query.get(article_id)
        if article == None:
            return flask.Response(status=404)
        else:
            db.session.delete(article)
            db.session.commit()
            return flask.Response(status=202)
    except:
        return flask.Response(status=400)
    

@app.route('/article/<article_id>/context', methods=['PUT'])
def update_article_context(article_id):
    if request.is_json:
        try:
            content = request.get_json()
            article = Article.query.get(article_id)
            if article == None:
                return "404: article not found"
            else:
                article.context = content['context']
                db.session.commit()
                return flask.Response(status=200)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=405)


@app.route('/article/<article_id>/status', methods=['PUT'])
def update_article_status(article_id):
    if request.is_json:
        try:
            content = request.get_json()
            article = Article.query.get(article_id)
            if article == None:
                return "404: article not found"
            else:
                article.status = content['status']
                db.session.commit()
            return flask.Response(status=200)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=405)


@app.route('/article/findByStatus', methods=['GET'])
def find_article_by_status():
    if request.is_json:
        try:
            content = request.get_json()
            articles = Article.query.filter_by(status= content['status'])
            output = []
            for article in articles:
                output.append(article.serialize())
            return json.dumps(output)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=405)

# <-------------------------->
# <----- Sentence calls ----->
# <-------------------------->

@app.route('/sentence', methods=['POST'])
def add_sentence():
    if request.is_json:
        try:
            content = request.get_json()
            to_add = Sentence(content['text'], content['article_id'])
            db.session.add(to_add)
            db.session.commit()
            return flask.Response(status=201)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=400)


@app.route('/sentence/findByStatus', methods=['GET'])
def find_sentence_by_status():
    if request.is_json:
        try:
            content = request.get_json()
            sentences = Sentence.query.filter_by(status=content['status'])
            output = []
            for sentence in sentences:
                output.append(sentence.serialize())
            return json.dumps(output)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=405)


@app.route('/sentence/<sentence_id>/', methods=['DELETE'])
def delete_sentence(sentence_id):
    try:
        content = request.get_json()
        sentence = Sentence.query.get(sentence_id)
        if sentence == None:
            return flask.Response(status=404)
        else:
            db.session.delete(sentence)
            db.session.commit()
            return flask.Response(status=200)
    except:
        return flask.Response(status=400)


@app.route('/sentence/<sentence_id>/context', methods=['PUT'])
def update_sentence_context(sentence_id):
    if request.is_json:
        try:
            content = request.get_json()
            sentence = Sentence.query.get(sentence_id)
            if sentence == None:
                return flask.Response(status=404)
            else:
                sentence.context = content['context']
                sentence.status = "SENTIMENT"
                db.session.commit()
                return flask.Response(status=200)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=405)


@app.route('/sentence/<sentence_id>/sentiment', methods=['PUT'])
def update_sentence_sentiment(sentence_id):
    if request.is_json:
        try:
            content = request.get_json()
            sentence = Sentence.query.get(sentence_id)
            if sentence == None:
                return flask.Response(status=404)
            else:
                sentence.sentiment = content['sentiment']
                sentence.status = "DONE"
                db.session.commit()
                return flask.Response(status=200)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=405)

# <------------------------->
# <----- Company calls ----->
# <------------------------->

@app.route('/company', methods=['POST'])
def add_company():
    if request.is_json:
        try:
            content = request.get_json()
            to_add = Company(content['stock_code'], content['short_hand'])
            try:
                db.session.add(to_add)
                db.session.commit()
                return flask.Response(status=201)
            except:
                return flask.Response(status=400)
        except:
            return flask.Response(status=400)
    else:
        return flask.Response(status=400)


@app.route('/company/<stock_code>', methods=['GET'])
def get_company(stock_code):
    try:
        company = Company.query.get(stock_code)
        if company == None:
            return flask.Response(status=404)
        else:
            return json.dumps(company.serialize())
    except:
        return flask.Response(status=405)


@app.route('/company/search/<short_hand>', methods=['GET'])
def search_for_company(short_hand):
    try:
        search = "%{}%".format(short_hand)
        companies = Company.query.filter(Company.short_hand.like(search)).all()
        output = []
        for company in companies:
            output.append(company.serialize())

        if output == []:
            return flask.Response(status=401)
        else:
            return json.dumps(output)
    except:
        return flask.Response(status=405)


@app.route('/company/<stock_code>/sentences', methods=['GET'])
def get_company_sentences(stock_code):
    try:
        sentences = Sentence.query.filter_by(context=stock_code).all()
        if sentences == []:
            return flask.Response(status=404)
        else:
            output = []
            for sentence in sentences:
                output.append(sentence.serialize())
            return json.dumps(output)
    except:
        return flask.Response(status=400)

# <---------------------------->
# <----- timeseries Calls ----->
# <---------------------------->


@app.route('/points/<company_id>', methods=['GET'])
def get_data_points(company_id):
    conn =psycopg2.connect(host='localhost',
                           port='5433',
                           user='postgres',
                           password='2206',
                           database='company_data')
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM points WHERE company_id= %s ORDER BY time DESC LIMIT 100", [company_id])
    points = json.dumps(cursor.fetchall(), indent=2, default=str)
    return points


@app.route('/points/<company_id>', methods=['POST'])
def add_data_point(company_id):
    conn = psycopg2.connect(host='localhost',
                            port='5433',
                            user='postgres',
                            password='2206',
                            database='company_data')
    cursor = conn.cursor()
    content = request.get_json()

    datetime_obj = datetime.strptime(content['time'], "%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO points(time, company_id, sentiment) VALUES(%s, %s, %s)",
                   [datetime_obj, company_id, content['sentiment']])
    conn.commit()

    return "Done"


if __name__ == '__main__':
    app.run()
