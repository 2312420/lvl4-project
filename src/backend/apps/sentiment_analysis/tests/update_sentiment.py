# Updates sentiment for sentences

import requests
import psycopg2

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


conn = psycopg2.connect(host='localhost',
                                port='5433',
                                user='postgres',
                                password='2206',
                                database='company_data')
cursor = conn.cursor()

toDo = len(sentences)
for sentence in sentences:
    sentence_id = sentence['id']

    # get sentiment score
    url = sentiment_url + "/sentiment"
    r = requests.get(url, json=sentence)
    result = r.json()

    sentence['sentiment'] = result['score']

    # Update sentiment score
    url = base_url + "/sentence/" + str(sentence['id']) + "/sentiment"
    r = requests.put(url, json=sentence)

    # Update status
    url = base_url + "/sentence/" +  str(sentence['id']) + "/status"
    r = requests.put(url, json={'status': "DONE"})

    # Update corresponding point
    cursor.execute("UPDATE points SET sentiment = %s WHERE sentence_id = %s ", [result['score'], sentence_id])
    conn.commit()

    toDo -= 1
    print(toDo)




