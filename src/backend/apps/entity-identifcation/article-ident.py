import psycopg2
import spacy
import requests

base_url = "http://127.0.0.1:5000"
nlp = spacy.load('en_core_web_sm')


# Get articles from db via api
def get_articles():
    url = base_url + '/article/findByStatus'
    payload = {"status": "CONTEXT"}
    r = requests.get(url, json=payload)
    return r.json()#r.json()22


# Analyse article transcript
def analyse(transcript):
    doc = nlp(transcript)
    orgs = []
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            orgs.append(ent.text)
    return orgs


# Updates article analyzed field
def update_article(article_id):
    url = base_url + "/article/" + article_id + "/status"
    payload = {"status": "SENTENCES"}
    r = requests.put(url, json=payload)


# Updates article context
def upload_entities(article_id, article_entites):
    url = base_url + "/article/" + article_id + "/context"
    payload = {"context": article_entites}
    r = requests.put(url, payload)


if __name__ == '__main__':
    while(True):
        for article in get_articles():
            id = article['id']
            entities = analyse(article['transcript'])
            upload_entities(id, entities)

