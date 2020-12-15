import modules as md
import json
import requests

import psycopg2
import psycopg2.extensions
import select

# Backend Api
base_url = "http://127.0.0.1:5000"

# DB connection
conn = psycopg2.connect(database="localdb", user="postgres", password="2206")


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
    print("sentence")
    if status == "CONTEXT":
        md.update_sentence_context(sentence)
    elif status == "SENTIMENT":
        md.sentence_sentiment(sentence)
    elif status == "PRED":
        pass


def process_article(article):
    print("article")
    status = article['status']
    if status == "CONTEXT":
        pass
    elif status == "SENTENCES":
        pass


if __name__ == '__main__':
    sentences = get_unfinished_sentences()
    articles = get_unfinished_articles()


    curs = conn.cursor()
    curs.execute("LISTEN sentence;")
    curs.execute("LISTEN article;")

    seconds_passed = 0
    print("Waiting for notifications on channel 'test'")
    while True:
        # Process unfinished sentences
        for sentence in sentences:
            process_sentence(sentence)
        for article in articles:
            process_article(article)

        conn.commit()
        # Seeing if notification has been triggered
        if select.select([conn], [], [], 5) == ([], [], []):
            seconds_passed += 5
            print(str(seconds_passed) + " seconds without notification...")
        else:
            seconds_passed = 0
            conn.poll()
            conn.commit()
            while conn.notifies:
                notify = conn.notifies.pop()
                sentences = get_unfinished_sentences()
                articles = get_unfinished_articles()

