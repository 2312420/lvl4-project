# Imports

from flask import Flask, request
import json
from textblob import TextBlob

baseurl = "http://127.0.0.1:5000"

app = Flask(__name__)


def get_sentiment_score(sentence):
    blob = TextBlob(sentence)
    return blob.sentiment.polarity


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
    #score = get_sentiment_score("This is AWFUL")
    #print(score)