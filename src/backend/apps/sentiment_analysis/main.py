# Imports

from flask import Flask, request
import json
from textblob import TextBlob

baseurl = "http://backend-api:5000"

app = Flask(__name__)


# Using textblobs gets sentiment score for sentence text
def get_sentiment_score(text):
    blob = TextBlob(text)
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
    app.run(host="0.0.0.0", port=5003)