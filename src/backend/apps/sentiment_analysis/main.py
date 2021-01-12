# Imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, request
import flask
import json
import requests

baseurl = "http://127.0.0.1:5000"

app = Flask(__name__)


# Analyses sentiment score of sentence
# will be replaced with more complex system if time permits
def get_sentiment_score(sentence):
    sent = SentimentIntensityAnalyzer()
    sent_dict = sent.polarity_scores(sentence)
    return sent_dict['compound']


@app.route('/', methods=['GET'])
def index():
    return "Sentiment api"


@app.route('/sentiment', methods=['GET'])
def get_sentence_sentiment():
    sentence = request.get_json()
    sentiment = get_sentiment_score(sentence['text'])
    return json.dumps({'score': sentiment})


if __name__ == "__main__":
    app.run(port=5003)
