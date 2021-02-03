# Updates context of sentences in DB without requiring full rerun

import requests

# Backend Api
base_url = "http://127.0.0.1:5000"
context_url = "http://127.0.0.1:5001"
pred_url = "http://127.0.0.1:5004/"

def get_articles():
    url = base_url + '/article/findByStatus'
    payload = {"status": "DONE"}
    r = requests.get(url, json=payload)
    return r.json()


def get_sentences():
    url = base_url + '/sentence/findByStatus'
    payload = {"status": "DONE"}
    r = requests.get(url, json=payload)
    return r.json()


# Update Article
for artilce in get_articles():
    url = context_url + "/ident/article"
    r = requests.get(url, json=artilce)

    context = r.json()
    url = base_url + "/article/" + context['article_id'] + '/context'
    r = requests.put(url, json=context)
    break

# Update Sentences
for sentence in get_sentences():
    url = context_url + "/ident/sentence"
    r = requests.get(url, json=sentence)
    context = r.json()

    url = base_url + "/sentence/" + str(sentence['id']) + "/context/only"
    r = requests.put(url, json=context)





