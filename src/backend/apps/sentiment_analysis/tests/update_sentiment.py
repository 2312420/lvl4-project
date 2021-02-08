# Updates sentiment for sentences

import requests

# Backend Api
base_url = "http://127.0.0.1:5000"
sentiment_url = "http://127.0.0.1:5003"

def get_sentences():
    url = base_url + '/sentence/findByStatus'
    payload = {"status": "DONE"}
    r = requests.get(url, json=payload)
    return r.json()


sentences = get_sentences()
todo = len(sentences)



for sentence in sentences:

    if sentence['sentiment'] == None:

        url = sentiment_url + "/sentiment"
        r = requests.get(url, json=sentence)
        result = r.json()

        sentence['sentiment'] = result['score']

        url = base_url + "/sentence/" + str(sentence['id']) + "/sentiment"
        r = requests.put(url, json=sentence)

        url = base_url + "/sentence/" +  str(sentence['id']) + "/status"
        r = requests.put(url, json={'status': "DONE"})

    todo -= 1
    print(todo)

