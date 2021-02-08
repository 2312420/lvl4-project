import requests
import csv
from datetime import datetime

url = "http://127.0.0.1:5003/sentiment"


def run_sentiment(text):
    payload = {'text': text}
    r = requests.get(url=url, json=payload)
    return r.json()['score']



def calcualte_metrics(title, pos_pos, pos_neg, pos_neu, acu):
    percision = pos_pos / (pos_pos + pos_neg + pos_neu)
    recall = pos_pos / acu
    f1 = 2 * ((percision * recall) / (percision + recall))
    return [title, percision, recall, f1]

def run_test(note):

    now = datetime.now()
    print(now)

    correct = 0
    incorret = 0

    false_neutral = 0
    false_positive = 0
    false_negative = 0

    total_pos = 0
    total_neg = 0
    total_neu = 0

    acu_pos = 0
    acu_neg = 0
    acu_neu = 0


    # Pred, Actual
    pos_pos = 0
    pos_neg = 0
    pos_neu = 0

    neg_pos = 0
    neg_neg = 0
    neg_neu = 0

    neu_pos = 0
    neu_neg = 0
    neu_neu = 0

    with open('data_sets/all-data.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        now = datetime.now().strftime("%d-%m-%Y, %H-%M")

        for row in csv_reader:
            text = row[0]
            real_sentiment = row[1]
            pred_sentiment = run_sentiment(text)

            if int(real_sentiment) == -1:
            # Sentiment is negative
                acu_neg += 1

                if pred_sentiment < 0:
                    correct += 1
                    neg_neg += 1
                else:
                    if pred_sentiment == 0:
                        false_neutral += 1
                        neu_neg += 1
                    else:
                        false_positive += 1
                        pos_neg += 1

            elif int(real_sentiment) == 1:
            # Sentiment is positive
                acu_pos += 1
                if pred_sentiment > 0:
                    correct += 1
                    pos_pos += 1
                else:
                    if pred_sentiment == 0:
                        false_neutral += 1
                        neu_pos += 1
                    else:
                        false_negative += 1
                        neg_pos += 1
                    incorret += 1

            else:
            # Sentiment is neutral
                acu_neu += 1
                if -0.3 <= pred_sentiment <= 0.3:
                    correct += 1
                    neu_neu += 1
                else:
                    if pred_sentiment < 0:
                        false_negative += 1
                        neg_neu += 1
                    else:
                        false_positive += 1
                        pos_neu += 1
                    incorret += 1


        with open('results/' + now + "(" + note + ").csv", "x") as o:
            csv_writer = csv.writer(o, delimiter=',',)
            csv_writer.writerow(['title', 'result'])
            csv_writer.writerow(['total sentences', correct + incorret])
            csv_writer.writerow(['correct', correct])
            csv_writer.writerow(['incorrect', incorret])
            csv_writer.writerow("CONFUSION MATRIX")
            csv_writer.writerow(["-", "-", "Positive", "Negative", "Neutral"])
            csv_writer.writerow(["-", "-", pos_neg + pos_neu + pos_pos, neg_neg + neg_neu + neg_pos, neu_pos + neu_neg + neu_neu])
            csv_writer.writerow(["Positive", acu_pos, pos_pos, neg_pos, neu_pos ])
            csv_writer.writerow(["Negative", acu_neg, pos_neg, neg_neg, neu_neg])
            csv_writer.writerow(["Neutral", acu_neu, pos_neu, neg_neu, neu_neu])
            csv_writer.writerow([now, datetime.now()])
            csv_writer.writerow(["METRIC MATRIX"])
            csv_writer.writerow(["-","Percision", "Recall", "f1 score"])
            csv_writer.writerow(calcualte_metrics("Positive", pos_pos, pos_neg, pos_neu, acu_pos))
            csv_writer.writerow(calcualte_metrics("Negative", neg_neg, neg_pos, neg_neu, acu_neg))
            csv_writer.writerow(calcualte_metrics("Neutral", neu_neu, neu_pos, neu_neg, acu_neu))


    print(now, datetime.now())

run_test("vader, new metrics")
