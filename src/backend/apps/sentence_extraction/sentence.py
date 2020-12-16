from flask import Flask, request
import flask
import json
import nltk.data
import requests

app = Flask(__name__)


# Divides text from article into list of sentences
def extract_sentences(article_transcript):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(article_transcript)
    return sentences


@app.route('/', methods=['GET'])
def index():
    return "Entity identification api"


@app.route('/sent', methods=['GET'])
def sentence_extraction():
    article = request.get_json()
    id = article['id']
    sentences = extract_sentences(article['transcript'])
    return json.dumps({'sentences': sentences})


if __name__ == '__main__':
    nltk.download('punkt')
    app.run(port=5002)
