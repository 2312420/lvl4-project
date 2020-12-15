from flask import Flask, request
import flask
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
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


# Gets sentences from db via api
#def get_sentences():
#    url = baseurl + '/sentence/findByStatus'
#    payload = {"status": "SENTIMENT"}
#    r = (requests.get(url, json=payload)).json()
#    return r

# Uploads sentiment score to db through api
#def update_sentiment(sentence_id, score):
#    url = baseurl + '/sentence/' + str(sentence_id) + "/sentiment"
#    payload = {"sentiment": score}
#    r = requests.put(url, json=payload)

#if __name__ == "__main__":
#    while True:
#        sentences = get_sentences()
#        for sentence in sentences:
#            sentiment = get_sentiment_score(sentence['text'])
#            update_sentiment(sentence['id'], sentiment)
#            print("Sentence sentiment analyzed")