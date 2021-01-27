from sentence_ident import analyse
import csv
from fuzzywuzzy import fuzz
from sentence_ident import analyse

#https://www.kaggle.com/rohitr4307/ner-dataset


def convert(lis_str):
    # Converts string into list
    new_lis = lis_str.replace("['", '')
    new_lis = new_lis.replace("']", '')
    new_lis = new_lis.split("', '")
    return new_lis


with open('data_sets/NER_Dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    # Metrics from http://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/
    truePositive = 0
    falseNegative = 0
    falsePositive = 0

    cor = 0
    inc = 0
    par = 0
    mis = 0
    spu = 0

    for row in csv_reader:
        if line_count != 0:
            text = row[1].replace("['", '').replace("']", '').replace("', '", ' ')
            text_lis = convert(row[1])
            objs = convert(row[3])

            valid_orgs = []
            for i in range(len(text_lis)):
                if objs[i] == "B-org":
                    valid_orgs.append(text_lis[i])

            print("valid:" + str(valid_orgs))
            our_orgs = analyse(text)
            print(our_orgs)

            for item in valid_orgs:
                if item in our_orgs:
                    print("True Positive")
                    our_orgs.remove(item)
                else:
                    print("False Negative")

            if len(our_orgs) > 0:
                print(len(our_orgs))



        line_count += 1






