from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
baseurl = "http://127.0.0.1:5000"

def get_sentiment_score(sentence):
    sent = SentimentIntensityAnalyzer()
    sent_dict = sent.polarity_scores(sentence)
    return sent_dict['compound']


def get_sentences():
    url = baseurl + '/sentence/findByStatus'
    payload = {"status": "SENTIMENT"}
    r = (requests.get(url, json=payload)).json()
    return r


def update_sentiment(sentence_id, score):
    url = baseurl + '/sentence/' + str(sentence_id) + "/sentiment"
    payload = {"sentiment": score}
    r = requests.put(url, json=payload)
    print(r)


if __name__ == "__main__":
    sentences = get_sentences()
    for sentence in sentences:
        sentiment = get_sentiment_score(sentence['text'])
        update_sentiment(sentence['id'], sentiment)



