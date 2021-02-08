# Imports
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, request
import json
import spacy
import en_core_web_sm

import stanza

from textblob import TextBlob

baseurl = "http://127.0.0.1:5000"

app = Flask(__name__)


# Analyses sentiment score of sentence
# will be replaced with more complex system if time permits
#def get_sentiment_score(sentence):
#    sent = SentimentIntensityAnalyzer()
#    sent_dict = sent.polarity_scores(sentence)
#    return sent_dict['compound']



#stanza.download('en', processors='tokenize,sentiment')

#def get_sentiment_score(sentence):
#    nlp = stanza.Pipeline(lang='en', processors='tokenize, sentiment')
#    doc = nlp(sentence)
#    for i, sentence in enumerate(doc.sentences):
#        print(i, sentence.sentiment)


#nlp = spacy.load("en_core_web_sm")
#
#def get_sentiment_score(sentence):
#    doc = nlp(sentence)
#    token_list = [token for token in doc if not token.is_stop]

#    lemmas = [f"Token: {token}, lemma: {token.lemma_}" for token in token_list ]
#    print(token_list[1].vector)


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
    #get_sentiment_score("This is Awful, worse and terrible")
