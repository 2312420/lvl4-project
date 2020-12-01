import spacy
import requests
from collections import Counter

base_url = "http://127.0.0.1:5000"
nlp = spacy.load('en_core_web_sm')


# Get sentences from db via api
def get_sentences():
    url = base_url + '/sentence/findByStatus'
    payload = {"status": "CONTEXT"}
    r = requests.get(url, json=payload)
    return r.json()


# Get article from db via api
def get_article(article_id):
    url = base_url + '/article/' + str(article_id)
    r = requests.get(url)
    return r.json()


# Fuzzy search for comapny in db
def search_for_company(short_hand):
    url = base_url + '/company/search/' + short_hand
    r = requests.get(url)
    return r


# Analyse sentences and get initial list of potential companies
def analyse(transcript):
    doc = nlp(transcript)
    orgs = []
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            orgs.append(ent.text)
    return orgs


# Create list ranking of possible companies
def context_list(parent_contexts, sentence_contexts):
    if not sentence_contexts:
        # No context can be gathered from sentence
        return Counter(parent_contexts)
    else:
        # Sentence pertains to some context
        #for item in parent_contexts:
        #    sentence_contexts.append(item)
        return Counter(sentence_contexts)


# Searches through context list to see if company available
def decider(parent_id, potential_context):
    article = get_article(parent_id)
    companies = context_list(article['context'], potential_context)
    for company in companies.keys():
        r = search_for_company(company)
        if r.status_code == 200:
            company = r.json()
            return company
    return None


# Updates article analyzed field
def update_sentence(sentence_id):
    url = base_url + "/sentence/" + sentence_id + "/context"
    payload = {"status": "SENTIMENT"}
    r = requests.put(url, json=payload)


if __name__ == '__main__':

    for sentence in get_sentences():
        potential_entities = analyse(sentence['text'])
        company = decider(sentence['article_id'], potential_entities)
        if company:
            print(company)
        else:
            print("No Company")


