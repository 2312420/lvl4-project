import modules as md
import requests
import os
from subprocess import *
import sys
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
    if status == "CONTEXT":
        md.update_sentence_context(sentence)
    elif status == "SENTIMENT":
        md.sentence_sentiment(sentence)
    elif status == "PRED":
        md.sentence_to_point(sentence)


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


args = sys.argv
cur_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':

    sentences = get_unfinished_sentences()
    articles = get_unfinished_articles()

    curs = conn.cursor()
    curs.execute("LISTEN sentence;")
    curs.execute("LISTEN article;")

    seconds_passed = 0
    print("Waiting for notifications")
    while True:
        updates = False
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

#if(args[1] == 'start' and args[2] == 'backend'):
#        print("Starting backend api...")
#        path = cur_path + '/backend_api/app.py'
#        backed_api = Popen(['python', path], shell=True, stdin=PIPE, stdout=PIPE)

#        print("Starting entity identification...")
#        path = cur_path + '/apps/entity_identification/main.py'
#        entity_ident = Popen(['python', path], shell=True, stdin=PIPE, stdout=PIPE)

#        print("Starting sentence extraction...")
#        path = cur_path + '/apps/sentence_extraction/sentence.py'
#        sentence_extraction = Popen(['python', path], shell=True, stdin=PIPE, stdout=PIPE)

#        print("Starting Sentiment analysis...")
#        path = cur_path + '/apps/sentiment_analysis/main.py'
#        sentiment_analysis = Popen(['python', path], shell=True, stdin=PIPE, stdout=PIPE)

#        print("Starting prediction...")
#        path = cur_path + '/apps/prediction/main.py'
#        prediction = Popen(['python', path], shell=True, stdin=PIPE, stdout=PIPE)
