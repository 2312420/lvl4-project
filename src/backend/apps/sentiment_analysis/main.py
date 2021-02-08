# Imports

from flask import Flask, request
import json
import spacy
import en_core_web_sm







baseurl = "http://127.0.0.1:5000"

app = Flask(__name__)


# VADER
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#def get_sentiment_score(sentence):
#    sent = SentimentIntensityAnalyzer()
#    sent_dict = sent.polarity_scores(sentence)
#    return sent_dict['compound']



# STANZA
# import stanza
#stanza.download('en', processors='tokenize,sentiment')
#def get_sentiment_score(sentence):
#    nlp = stanza.Pipeline(lang='en', processors='tokenize, sentiment')
#    doc = nlp(sentence)
#    for i, sentence in enumerate(doc.sentences):
#        print(sentence)


# TEXT BLOB
from textblob import TextBlob
def get_sentiment_score(sentence):
    blob = TextBlob(sentence)
    return blob.sentiment.polarity


# NLTK
#import nltk
#nltk.download('vader_lexicon')
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nlp = SentimentIntensityAnalyzer()
#def get_sentiment_score(sentence):
#    score = nlp.polarity_scores(sentence)
#    return score['compound']

# Flair
#import flair

#flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
#def get_sentiment_score(sentence):
#    s = flair.data.Sentence(sentence)
#    flair_sentiment.predict(s)
#    val = s.labels[0].to_dict()['value']
#    if val == 'POSITIVE':
#        score = s.to_dict()['labels'][0]['confidence']
#    else:
#        score = -(s.to_dict()['labels'][0]['confidence'])
#    return score


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