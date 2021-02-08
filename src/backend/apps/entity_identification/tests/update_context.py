# Updates context of sentences in DB without requiring full rerun

import requests
import datetime

# Backend Api
base_url = "http://127.0.0.1:5000"
context_url = "http://127.0.0.1:5001"
pred_url = "http://127.0.0.1:5004/"

def get_articles():
    url = base_url + '/article/findByStatus'
    payload = {"status": "REDO"}
    r = requests.get(url, json=payload)
    return r.json()


def get_sentences():
    url = base_url + '/sentence/findByStatus'
    payload = {"status": "REDO"}
    r = requests.get(url, json=payload)
    return r.json()


start = datetime.datetime.now()

print(start)

# Update Article

#articles = get_articles()
#line = len(articles)
#for artilce in articles:
#    try:
#        url = context_url + "/ident/article"
#        r = requests.get(url, json=artilce)
#        context = r.json()
#        artilce['context'] = context['context']
#        artilce['status'] = "DONE"
#        url = base_url + "/update_article"
#        r = requests.put(url, json=artilce)
#    except:
#        print("Something went wrong")
#    line -= 1
#    print(line)


print("---------------------------------------------------")


line = 0
# Update Sentences
sentences = get_sentences()
line = len(sentences)
for sentence in sentences:

    url = context_url + "/ident/sentence"
    r = requests.get(url, json=sentence)
    if r.status_code == 200:
        context = r.json()
        if context:
            url = base_url + "/sentence/" + str(sentence['id']) + "/context/only"
            r = requests.put(url, json=context)
            url = base_url + "/sentence/" + str(sentence['id']) + "/status"
            r = requests.put(url, json={'status': 'DONE'}) 
            print("Sentence Done")

    elif r.status_code == 204:
        url = base_url + "/sentence/" + str(sentence['id']) + "/status"
        r = requests.put(url, json={'status': 'BLOCKED'})
        print("Blocked")
    else:
        print("Something went wrong")
    line -= 1
    print(line)


print("---FINISHED---")
print(start)
print(datetime.datetime.now())



