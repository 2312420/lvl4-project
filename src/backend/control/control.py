import modules as md
import requests
import os
from subprocess import *
import sys
import psycopg2
import psycopg2.extensions
import select

# Backend Api
base_url = "http://backend-api:5000"

# Backend component urls
entity_ident_url = "http://entity-ident:5001/ident"
sentence_extraction_url = "http://sentence-extraction:5002/"
sentence_sentiment_url = "http://sentiment-analysis:5003/"
prediction_url = "http://prediction:5004/"





def wait(url):
    response = False
    while True:
        try:
            r = requests.get(url)
            print(r.status_code)
            if r.status_code == 200:
                break
        except:
            pass

# Get list of unfinished sentences
def get_unfinished_sentences():
    statuses = ["CONTEXT", "SENTIMENT", "PRED"]
    url = base_url + "/sentence/findByStatus"
    sentences = []
    for status in statuses:
        payload = {'status': status}
        r = requests.get(url, json=payload)
        for sentence in r.json():
            sentences.append(sentence)
    return sentences


# Get list of unfinished articles
def get_unfinished_articles():
    statuses = ["CONTEXT", "SENTENCES"]
    url = base_url + "/article/findByStatus"
    articles = []
    for status in statuses:
        payload = {'status': status}
        r = requests.get(url, json=payload)
        for article in r.json():
            articles.append(article)
    return articles


def process_sentence(sentence):
    status = sentence['status']
    if status == "CONTEXT":
        md.update_sentence_context(sentence)
    elif status == "SENTIMENT":
        md.sentence_sentiment(sentence)
    elif status == "PRED":
        md.sentence_to_point(sentence)
        # New point has been added so update prediction for company
        md.company_prediction(sentence['context'])


def process_article(article):
    status = article['status']
    if status == "CONTEXT":
        md.update_article_context(article)
    elif status == "SENTENCES":
        md.article_sentence_extraction(article)


def process(articles, sentences):
    for article in articles:
        process_article(article)
    for sentence in sentences:
        process_sentence(sentence)
    return [], []


if __name__ == '__main__':

    # DB connection
    while True:
        try:
            conn = psycopg2.connect(host='dbmain',
                                    port='5432',
                                    user='postgres',
                                    password='2206',
                                    database='maindb')
            print("Connected to db")
            break
        except:
            pass

    wait(sentence_extraction_url)
    print("connected to sentence extraction component")
    wait(entity_ident_url)
    print("connected to entity identification component")
    wait(sentence_sentiment_url)
    print("connected to sentence sentiment component")
    wait(prediction_url)
    print("connected to prediction component")

    sentences = get_unfinished_sentences()
    articles = get_unfinished_articles()

    curs = conn.cursor()
    curs.execute("LISTEN sentence;")
    curs.execute("LISTEN article;")

    seconds_passed = 0
    print("Waiting for notifications")
    updates = False

    while True:
        if sentences != [] or articles != []:
            # Articles and sentences to be processed
            sentences, articles = process(articles, sentences)
            updates = True

        conn.commit()
        # Seeing if notification has been triggered
        if select.select([conn], [], [], 5) == ([], [], []):
            seconds_passed += 5
            print(str(seconds_passed) + " seconds without notification...")
        else:
            updates = True
            seconds_passed = 0
            conn.poll()
            conn.commit()
            while conn.notifies:
                notify = conn.notifies.pop()
                sentences = get_unfinished_sentences()
                articles = get_unfinished_articles()
