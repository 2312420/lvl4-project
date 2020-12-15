# Libs
from flask import Flask, request
import flask
import json
import requests

# Ident files
import sentence_ident as si

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


@app.route('/ident/article')
def article_ident():
    content = request.get_json()


if __name__ == '__main__':
    app.run(port=5001)