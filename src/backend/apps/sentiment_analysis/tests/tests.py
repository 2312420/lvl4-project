import requests
import csv

url = "http://127.0.0.1:5003/sentiment"


def run_sentiment(text):
    payload = {'text': text}
    r = requests.get(url=url, json=payload)
    return r.json()['score']


def run_test():
    correct = 0
    incorret = 0

    false_neutral = 0
    false_positive = 0
    false_negative = 0

    with open('data_sets/all-data.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
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
        
        print("total sentences:" + str(correct + incorret))
        print("correct        :" + str(correct))
        print("incorrect      :" + str(incorret))
        print("false neutral  :" + str(false_neutral))
        print("false negative :" + str(false_negative))
        print("false positive :" + str(false_positive))





run_test()