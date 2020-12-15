import sys
import requests
import json

# Component Apis
article_context = "http://127.0.0.1:5001/ident/article"
sentence_context = "http://127.0.0.1:5001/ident/sentence"
sentence_extraction_url = "http://127.0.0.1:5002/sent"

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


if __name__ == '__main__':
    for article in get_articles_for_extract():
        article_sentence_extraction(article)



