import nltk.data
import requests

base_url = "http://127.0.0.1:5000/"


# Gets 10 articles from database
def get_articles():
    url = base_url + 'article/findByStatus'
    payload = {"status": "SENTENCES"}
    r = requests.get(url, json=payload)
    return r.json()#r.json()22


# Divides text from article into list of sentences
def extract_sentences(article_transcript):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(article_transcript)
    return sentences


# Updates article analyzed field
def update_article(article_id):
    url = base_url + "article/" + article_id + "/status"
    payload = {"status": "DONE"}
    r = requests.put(url, json=payload)


# Uploads sentences to database
def upload_sentence(article_id, article_sentence, article_date, article_time):
    url = base_url + "sentence"
    payload = {"text": article_sentence, "article_id": article_id, "date": article_date, "time": article_time}
    r = requests.post(url, json=payload)


if __name__ == '__main__':
    nltk.download('punkt')
    while True:
        articles = get_articles()
        for article in articles:
            id = article['id']
            update_article(id)
            for sentence in extract_sentences(article['transcript']):
                upload_sentence(id, sentence, article['date'], article['time'])
            print("Article sentences extracted")