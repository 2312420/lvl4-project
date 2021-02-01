from sentence_ident import analyse
import csv
from fuzzywuzzy import fuzz
from sentence_ident import analyse
from datetime import datetime

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
            text_lis = text.split(" ")#convert(row[1])
            objs = convert(row[3])


            valid_orgs = []
            for i in range(len(text_lis)):
                if objs[i] == "B-org":
                    valid_orgs.append(text_lis[i])
                elif objs[i] == "I-org":
                    valid_orgs[-1] = valid_orgs[-1] + " " + text_lis[i]

            our_orgs = analyse(text)

            #if valid_orgs != [] and our_orgs != []:
            #    print(valid_orgs)
            #    print(our_orgs)
            #    print("-------")

            correct = 0
            for our in our_orgs:
                found = False
                for valid in valid_orgs:
                    ratio = fuzz.ratio(our, valid)
                    if ratio >= 60:
                        correct += 1

            truePositive += correct
            falsePositive += len(our_orgs) - correct
            falseNegative += len(valid_orgs) - correct
        line_count += 1
        print(line_count)
        if line_count == 20000:
            break
    
    """
    now = datetime.now().strftime("%d-%m-%Y, %H-%M")
    note = "SpacyNLP(minorFix)"
    with open('results/' + now + "(" + note + ").csv", "x") as o:
        csv_writer = csv.writer(o, delimiter=',', )
        csv_writer.writerow(['title', 'result'])
        csv_writer.writerow(['truePositive', truePositive])
        csv_writer.writerow(['falsePositive', falsePositive])
        csv_writer.writerow(['falseNegative', falseNegative])
        csv_writer.writerow(['Percision', (truePositive / (truePositive + falsePositive))])
        csv_writer.writerow(['True Positive Rate', (truePositive / (truePositive + falseNegative))])
    """





