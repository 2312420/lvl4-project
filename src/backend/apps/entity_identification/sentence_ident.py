import requests
import common as c
from collections import Counter


base_url = "http://backend-api:5000"
#nlp = spacy.load('en_core_web_sm')


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
    doc = c.get_entities(transcript)
    orgs = []
    for ent in doc.ents:
        if ent.type == 'ORG':
            orgs.append(ent.text)
    return orgs


# Given a list of companies fuzzy searches db through api for company
def find_company(company_list):
    for company in company_list:
        r = search_for_company(company)
        if r.status_code == 200:
            # Company has been found
            company = r.json()
            return company
    return None


# Decides if company context comes from article or sentence
def decider(parent_id, potential_context):
    companies = Counter(potential_context).keys()
    company = find_company(companies)
    if company == None:
        article = get_article(parent_id)
        return find_company(Counter(article['context']).keys())
    else:
        return company


# Get sentences from db via api
#def get_sentences():
#    url = base_url + '/sentence/findByStatus'
#    payload = {"status": "CONTEXT"}
#    r = requests.get(url, json=payload)
#    return r.json()

# Get article from db via api
#def get_article(article_id):
#    url = base_url + '/article/' + str(article_id)
#    r = requests.get(url)
#    return r.json()

# Updates article analyzed field
#def update_sentence(sentence_id, stock_code):
#    url = base_url + "/sentence/" + str(sentence_id) + "/context"
#    payload = {"context": stock_code}
#    r = requests.put(url, json=payload)

#if __name__ == '__main__':
#    while True:
#        for sentence in get_sentences():
#            potential_entities = analyse(sentence['text'])
#            company = decider(sentence['article_id'], potential_entities)
#            if company:
#                update_sentence(sentence['id'], company[0]['stock_code'])
#            print("sentence analyzed")