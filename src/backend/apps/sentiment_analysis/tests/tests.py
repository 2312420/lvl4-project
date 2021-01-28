import requests
import csv
from datetime import datetime

url = "http://127.0.0.1:5003/sentiment"


def run_sentiment(text):
    payload = {'text': text}
    r = requests.get(url=url, json=payload)
    return r.json()['score']


def run_test(note):
    correct = 0
    incorret = 0

    false_neutral = 0
    false_positive = 0
    false_negative = 0

    with open('data_sets/all-data.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        now = datetime.now().strftime("%d-%m-%Y, %H-%M")

        for row in csv_reader:
            text = row[0]
            real_sentiment = row[1]
            pred_sentiment = run_sentiment(text)

            if real_sentiment == -1:
            # Sentiment is negative
                if pred_sentiment < 0:
                    correct += 1
                else:
                    if pred_sentiment == 0:
                        false_neutral += 1
                    else:
                        false_positive += 1

            elif real_sentiment == 1:
            # Sentiment is positive
                if pred_sentiment > 0:
                    correct += 1
                else:
                    if pred_sentiment == 0:
                        false_neutral += 1
                    else:
                        false_negative += 1
                    incorret += 1

            else:
            # Sentiment is neutral
                if -0.3 <= pred_sentiment <= 0.3:
                    correct += 1
                else:
                    if pred_sentiment < 0:
                        false_negative += 1
                    else:
                        false_positive += 1
                    incorret += 1

        with open('results/' + now + "(" + note + ").csv", "x") as o:
            csv_writer = csv.writer(o, delimiter=',',)
            csv_writer.writerow(['title', 'result'])
            csv_writer.writerow(['total sentences', correct + incorret])
            csv_writer.writerow(['correct', correct])
            csv_writer.writerow(['incorrect', incorret])
            csv_writer.writerow(['false neutral', false_neutral])
            csv_writer.writerow(['false negative', false_negative])
            csv_writer.writerow(['false positive', false_positive])



run_test("vaderSentiment")