# Libs
from flask import Flask, request
import flask
import json
import requests

# Ident files
import sentence_ident as si
import article_ident as ai

app = Flask(__name__)


@app.route('/ident', methods=['GET'])
def index():
    return "Entity identification api"


@app.route('/ident/sentence', methods=['GET'])
def sentence_ident():
    sentence = request.get_json()
    potential_entities = si.analyse(sentence['text'])
    company = si.decider(sentence['article_id'], potential_entities)

    if company:
        return json.dumps({"sentence_id": sentence['id'], "context": company[0]['stock_code']})
    else:
        return flask.Response(status=204)


@app.route('/ident/article', methods=['GET'])
def article_ident():
    article = request.get_json()
    entites = ai.analyse(article['transcript'])
    return json.dumps({"article_id": article['id'], "context": entites})


if __name__ == '__main__':
    app.run(port=5001)