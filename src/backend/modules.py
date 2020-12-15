import sys
import requests
import json

# Component Apis
article_context = "http://127.0.0.1:5001/ident/article"
sentence_context = "http://127.0.0.1:5001/ident/sentence"
sentence_extraction_url = "http://127.0.0.1:5002/sent"
sentence_sentiment_url = "http://127.0.0.1:5003/sentiment"
prediction_base_url = "http://127.0.0.1:5004"

# Backend Api
base_url = "http://127.0.0.1:5000"


# <!-------------------------!> #
# <!--- CONTEXT FUNCTIONS ---!> #
# <!-------------------------!> #

# Gets sentence context and updates database
def update_sentence_context(sentence):
    r = requests.get(url=sentence_context, json=sentence)
    if r.status_code == 200:
        content = r.json()
        url = base_url + "/sentence/" + str(content['sentence_id']) + "/context"
        payload = {"context": content['context']}
        r = requests.put(url, json=payload)


def update_article_context(article):
    r = requests.get(url=article_context, json=article)
    if r.status_code == 200:
        content = r.json()

        ## upload entities
        url = base_url + "/article/" + content['article_id'] + "/context"
        payload = {"context": content['context']}
        r = requests.put(url, json=payload)

        ## update status
        url = base_url + "/article/" + content['article_id'] + "/status"
        payload = {"status": "SENTENCES"}
        r = requests.put(url, json=payload)


def get_sentences():
    url = base_url + '/sentence/findByStatus'
    payload = {"status": "CONTEXT"}
    r = requests.get(url, json=payload)
    return r.json()


def get_articles_context():
    url = base_url + '/article/findByStatus'
    payload = {"status": "CONTEXT"}
    r = requests.get(url, json=payload)
    return r.json()#r.json()22


# <!-------------------------!> #
# <!---- SENT EXTRACTION ----!> #
# <!-------------------------!> #

def article_sentence_extraction(article):
    r = requests.get(sentence_extraction_url, json=article)
    if r.status_code == 200:
        content = r.json()

        # Update article status
        url = base_url + "/article/" + article['id'] + "/status"
        payload = {"status": "DONE"}
        r = requests.put(url, json=payload)

        # Upload sentences
        url = base_url + "/sentence"
        for sentence in content['sentences']:
            payload = {"text": sentence, "article_id": article['id'], "date": article['date'], "time": article['time']}
            r = requests.post(url, json=payload)


def get_articles_for_extract():
    url = base_url + '/article/findByStatus'
    payload = {"status": "SENTENCES"}
    r = requests.get(url, json=payload)
    return r.json()


# <!-------------------------!> #
# <!-- SENTIMENT FUNCTIONS --!> #
# <!-------------------------!> #


def sentence_sentiment(sentence):
    r = requests.get(sentence_sentiment_url, json=sentence)
    if r.status_code == 200:
        content = r.json()
        url = base_url + '/sentence/' + str(sentence['id']) + "/sentiment"
        payload = {"sentiment": content['score']}
        r = requests.put(url, json=payload)
        print(r.status_code)


def get_sentences_for_sentiment():
    url = base_url + '/sentence/findByStatus'
    payload = {"status": "SENTIMENT"}
    r = (requests.get(url, json=payload)).json()
    return r


# <!-------------------------!> #
# <!------- PREDICTION ------!> #
# <!-------------------------!> #


# Standard prediction on company
def company_prediction(company):
    url = prediction_base_url + "/predictions"
    r = requests.get(url, json=company)
    if r.status_code == 200:
        content = r.json()
        url = base_url + '/company/predictions'
        payload = {'stock_code': content['stock_code'], 'verdict': content['verdict'], 'predictions': content['new_preds']}
        r = requests.post(url, json=payload)


# Take sentences and turns them into data points
def sentence_to_point(sentence):
    url = prediction_base_url + "/points/sentences"
    r = requests.post(url=url, json=sentence)
    if r.status_code == 200:
        print("Point updated")


# Get all companies from db
def get_companies():
    url = base_url + "/company"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None


# Get all sentences that need to be transformed into points
def get_sentences():
    url = base_url + "/sentence/findByStatus"
    payload = {"status": "PRED"}
    r = requests.get(url, json=payload)
    if r.status_code == 200:
        return r.json()
    else:
        return None